using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class Tile : MonoBehaviour
{
    public TileState State { get; private set; }
    public TileCell Cell { get; private set; }
    public int Number { get; private set; }
    public bool Locked { get; set; }
    private Image background;
    private TextMeshProUGUI text;
    private void Awake()
    {
        background = GetComponent<Image>();
        text = GetComponentInChildren<TextMeshProUGUI>();
    }
    public void SetState(TileState state, int number)
    {
        this.State = state;
        this.Number = number;

        background.color = state.backgroundColor;
        text.color = state.textColor;
        text.text = number.ToString();
    }

    public void Spawn(TileCell cell)
    {
        if (this.Cell != null)
        {
            this.Cell.Tile = null;
        }

        this.Cell = cell;
        this.Cell.Tile = this;

        transform.position = cell.transform.position;
    }
    public void MoveTo(TileCell cell)
    {
        if (this.Cell != null)
        {
            this.Cell.Tile = null;
        }

        this.Cell = cell;
        this.Cell.Tile = this;

        StartCoroutine(Animate(cell.transform.position, false));
    }
    public void Merge(TileCell cell)
    {
        if (this.Cell != null)
        {
            this.Cell.Tile = null;
        }
        this.Cell = null;
        cell.Tile.Locked = true;

        StartCoroutine(Animate(cell.transform.position, true));
    }
    private IEnumerator Animate(Vector3 to, bool merging)
    {
        float elapsed = 0f;
        float duration = 0.1f;

        Vector3 from = transform.position;

        while (elapsed < duration)
        {
            transform.position = Vector3.Lerp(from, to, elapsed / duration);
            elapsed += Time.deltaTime;
            yield return null;
        }

        transform.position = to;

        if (merging)
        {
            Destroy(gameObject);
        }
    }
}
