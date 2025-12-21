using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;
using Unity.VisualScripting;
using System.Data;

// Управляет игровой доской: обработка ввода, перемещение плиток, слияние и проверка окончания игры
public class TileBoard : MonoBehaviour
{
    public GameManager gameManager;
    public Tile TilePrefab;
    public TileState[] TileStates;
    private TileGrid Grid;
    private List<Tile> Tiles;
    private bool waiting; // Флаг ожидания завершения анимации перед следующим ходом

    // Инициализация компонентов при создании объекта
    private void Awake()
    {
        Grid = GetComponentInChildren<TileGrid>();
        Tiles = new List<Tile>(16); // Максимум 16 плиток на доске 4x4
    }
    
    // Очищает доску: удаляет все плитки и освобождает ячейки
    public void ClearBoard()
    {
        // Освобождаем все ячейки
        foreach (var cell in Grid.Cells)
        {
            cell.Tile = null;
        }
        
        // Уничтожаем все плитки
        foreach (var tile in Tiles)
        {
            Destroy(tile.gameObject);
        }
        Tiles.Clear();
    }
    
    // Создает новую плитку со значением 2 в случайной пустой ячейке
    public void CreateTile()
    {
        Tile tile = Instantiate(TilePrefab, Grid.transform);
        tile.SetState(TileStates[0], 2); // Первое состояние всегда соответствует значению 2
        tile.Spawn(Grid.GetRandomEmptyCell());
        Tiles.Add(tile);
    }

    // Обработка ввода с клавиатуры для перемещения плиток
    private void Update()
    {
        if (!waiting)
        {
            // Движение вверх (W или стрелка вверх)
            if (Keyboard.current.wKey.wasPressedThisFrame || Keyboard.current.upArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.up, 0, 1, 1, 1);
            }
            // Движение влево (A или стрелка влево)
            else if (Keyboard.current.aKey.wasPressedThisFrame || Keyboard.current.leftArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.left, 1, 1, 0, 1);
            }
            // Движение вниз (S или стрелка вниз)
            else if (Keyboard.current.sKey.wasPressedThisFrame || Keyboard.current.downArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.down, 0, 1, Grid.Height - 2, -1);
            }
            // Движение вправо (D или стрелка вправо)
            else if (Keyboard.current.dKey.wasPressedThisFrame || Keyboard.current.rightArrowKey.wasPressedThisFrame)
            {
                MoveTiles(Vector2Int.right, Grid.Width - 2, -1, 0, 1);
            }
        }
    }

    // Перемещает все плитки в указанном направлении
    private void MoveTiles(Vector2Int direction, int startX, int incrementX, int startY, int incrementY)
    {
        bool changed = false;

        // Обход ячеек в правильном порядке для корректного перемещения
        for (int x = startX; x >= 0 && x < Grid.Width; x += incrementX)
        {
            for (int y = startY; y >= 0 && y < Grid.Height; y += incrementY)
            {
                TileCell cell = Grid.GetCell(x, y);

                // Перемещаем плитку, если ячейка занята
                if (cell.Occupied)
                {
                    changed |= MoveTile(cell.Tile, direction);
                }
            }
        }

        // Если были изменения, ждем завершения анимации и создаем новую плитку
        if (changed)
        {
            StartCoroutine(WaitForChanges());
        }
    }
    
    // Перемещает одну плитку в указанном направлении
    private bool MoveTile(Tile tile, Vector2Int direction)
    {
        TileCell newCell = null;
        TileCell adjacent = Grid.GetAdjacentCell(tile.Cell, direction);

        // Ищем самую дальнюю доступную ячейку в направлении движения
        while (adjacent != null)
        {
            if (adjacent.Occupied)
            {
                // Если ячейка занята, проверяем возможность слияния
                if (CanMerge(tile, adjacent.Tile))
                {
                    Merge(tile, adjacent.Tile);
                    return true;
                }

                // Если слияние невозможно, останавливаемся
                break;
            }

            newCell = adjacent;
            adjacent = Grid.GetAdjacentCell(adjacent, direction);
        }

        // Перемещаем плитку в найденную ячейку
        if (newCell != null)
        {
            tile.MoveTo(newCell);
            return true;
        }

        return false;
    }

    // Проверяет, могут ли две плитки быть объединены
    private bool CanMerge(Tile a, Tile b)
    {
        return a.Number == b.Number && !b.Locked;
    }

    // Объединяет две плитки: уничтожает первую и удваивает значение второй
    private void Merge(Tile a, Tile b)
    {
        Tiles.Remove(a);
        a.Merge(b.Cell);

        // Находим следующее состояние для объединенной плитки
        int index = Mathf.Clamp(IndexOf(b.State) + 1, 0, TileStates.Length - 1);
        int number = b.Number * 2;

        // Обновляем состояние и значение плитки
        b.SetState(TileStates[index], number);

        // Увеличиваем счет на значение объединенной плитки
        gameManager.IncreaseScore(number);
    }

    // Находит индекс состояния плитки в массиве TileStates
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

    // Корутина ожидания завершения анимации перед следующим действием
    private IEnumerator WaitForChanges()
    {
        waiting = true;

        // Ждем завершения анимации
        yield return new WaitForSeconds(0.1f);

        waiting = false;

        // Разблокируем все плитки для следующего хода
        foreach (var tile in Tiles)
        {
            tile.Locked = false;
        }

        // Создаем новую плитку, если есть свободные ячейки
        if (Tiles.Count != Grid.Size)
        {
            CreateTile();
        }

        // Проверяем условие окончания игры
        if (CheckForGameOver())
        {
            gameManager.GameOver();
        }
    }

    // Проверяет, закончилась ли игра (нет возможных ходов)
    private bool CheckForGameOver()
    {
        // Если есть свободные ячейки, игра не окончена
        if (Tiles.Count != Grid.Size)
        {
            return false;
        }

        // Проверяем каждую плитку на возможность слияния с соседями
        foreach (var tile in Tiles)
        {
            TileCell up = Grid.GetAdjacentCell(tile.Cell, Vector2Int.up);
            TileCell left = Grid.GetAdjacentCell(tile.Cell, Vector2Int.left);
            TileCell down = Grid.GetAdjacentCell(tile.Cell, Vector2Int.down);
            TileCell right = Grid.GetAdjacentCell(tile.Cell, Vector2Int.right);

            // Если хотя бы одно слияние возможно, игра продолжается
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
        
        // Нет возможных ходов - игра окончена
        return true;
    }
}
