using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;
using Unity.VisualScripting;
using System.Data;

public class TileBoard : MonoBehaviour
{
    public GameManager gameManager;
    public Tile TilePrefab;
    public TileState[] TileStates;
    private TileGrid Grid;
    private List<Tile> Tiles;

    private bool waiting;

    private void Awake()
    {
        Grid = GetComponentInChildren<TileGrid>();
        Tiles = new List<Tile>(16);
    }
    public void ClearBoard()
    {
        foreach (var cell in Grid.Cells)
        {
            cell.Tile = null;
        }
        foreach (var tile in Tiles)
        {
            Destroy(tile.gameObject);
        }
        Tiles.Clear();
    }
    public void CreateTile()
    {
        Tile tile = Instantiate(TilePrefab, Grid.transform);
        tile.SetState(TileStates[0], 2);
        tile.Spawn(Grid.GetRandomEmptyCell());
        Tiles.Add(tile);
    }

    private void Update()
    {
        if (!waiting)
        {
            if (Keyboard.current.wKey.wasPressedThisFrame || Keyboard.current.upArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.up, 0, 1, 1, 1);
            }
            else if (Keyboard.current.aKey.wasPressedThisFrame || Keyboard.current.leftArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.left, 1, 1, 0, 1);
            }
            else if (Keyboard.current.sKey.wasPressedThisFrame || Keyboard.current.downArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.down, 0, 1, Grid.Height - 2, -1);
            }
            else if (Keyboard.current.dKey.wasPressedThisFrame || Keyboard.current.rightArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.right, Grid.Width - 2, -1, 0, 1);
            }
        }
    }

    private void MoveTiles(Vector2Int direction, int startX, int incrementX, int startY, int incrementY)
    {
        bool changed = false;

        for (int x = startX; x >= 0 && x < Grid.Width; x += incrementX)
        {
            for (int y = startY; y >= 0 && y < Grid.Height; y += incrementY)
            {
                TileCell cell = Grid.GetCell(x, y);

                if (cell.Occupied)
                {
                    changed |= MoveTile(cell.Tile, direction);
                }
            }
        }

        if (changed)
        {
            StartCoroutine(WaitForChanges());
        }
    }
    private bool MoveTile(Tile tile, Vector2Int direction)
    {
        TileCell newCell = null;
        TileCell adjacent = Grid.GetAdjacentCell(tile.Cell, direction);

        while (adjacent != null)
        {
            if (adjacent.Occupied)
            {
                if (CanMerge(tile, adjacent.Tile))
                {
                    Merge(tile, adjacent.Tile);
                    return true;
                }

                break;
            }

            newCell = adjacent;
            adjacent = Grid.GetAdjacentCell(adjacent, direction);
        }

        if (newCell != null)
        {
            tile.MoveTo(newCell);

            return true;
        }

        return false;
    }

    private bool CanMerge(Tile a, Tile b)
    {
        return a.Number == b.Number && !b.Locked;
    }

    private void Merge(Tile a, Tile b)
    {
        Tiles.Remove(a);
        a.Merge(b.Cell);

        int index = Mathf.Clamp(IndexOf(b.State) + 1, 0, TileStates.Length - 1);
        int number = b.Number * 2;

        b.SetState(TileStates[index], number);

        gameManager.IncreaseScore(number);
    }

    private int IndexOf(TileState state)
    {
        for (int i = 0; i < TileStates.Length; i++)
        {
            if (state == TileStates[i])
            {
                return i;
            }
        }

        return -1;
    }

    private IEnumerator WaitForChanges()
    {
        waiting = true;

        yield return new WaitForSeconds(0.1f);

        waiting = false;

        foreach (var tile in Tiles)
        {
            tile.Locked = false;
        }

        if (Tiles.Count != Grid.Size)
        {
            CreateTile();
        }

        if (CheckForGameOver())
        {
            gameManager.GameOver();
        }
    }

    private bool CheckForGameOver()
    {
        if (Tiles.Count != Grid.Size)
        {
            return false;
        }

        foreach (var tile in Tiles)
        {
            TileCell up = Grid.GetAdjacentCell(tile.Cell, Vector2Int.up);
            TileCell left = Grid.GetAdjacentCell(tile.Cell, Vector2Int.left);
            TileCell down = Grid.GetAdjacentCell(tile.Cell, Vector2Int.down);
            TileCell right = Grid.GetAdjacentCell(tile.Cell, Vector2Int.right);

            if (up != null && CanMerge(tile, up.Tile))
            {
                return false;
            }
            if (left != null && CanMerge(tile, left.Tile))
            {
                return false;
            }
            if (down != null && CanMerge(tile, down.Tile))
            {
                return false;
            }
            if (right != null && CanMerge(tile, right.Tile))
            {
                return false;
            }
        }
        return true;
    }
}
