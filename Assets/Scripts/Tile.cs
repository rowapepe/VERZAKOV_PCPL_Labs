using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

// Класс, представляющий отдельную плитку на игровой доске
public class Tile : MonoBehaviour
{
    public TileState State { get; private set; }
    public TileCell Cell { get; private set; }
    public int Number { get; private set; }
    public bool Locked { get; set; }
    private Image background;
    private TextMeshProUGUI text;
    
    // Инициализация компонентов при создании объекта
    private void Awake()
    {
        background = GetComponent<Image>();
        text = GetComponentInChildren<TextMeshProUGUI>();
    }
    
    // Устанавливает состояние плитки и обновляет визуальное отображение
    public void SetState(TileState state, int number)
    {
        this.State = state;
        this.Number = number;

        // Обновление визуального представления
        background.color = state.backgroundColor;
        text.color = state.textColor;
        text.text = number.ToString();
    }

    // Начальное появление плитки в указанной ячейке без анимации
    public void Spawn(TileCell cell)
    {
        // Освобождаем предыдущую ячейку, если она была
        if (this.Cell != null)
        {
            this.Cell.Tile = null;
        }

        // Устанавливаем новую ячейку
        this.Cell = cell;
        this.Cell.Tile = this;

        // Мгновенное появление без анимации
        transform.position = cell.transform.position;
    }
    
    // Перемещает плитку в указанную ячейку с анимацией
    public void MoveTo(TileCell cell)
    {
        // Освобождаем предыдущую ячейку
        if (this.Cell != null)
        {
            this.Cell.Tile = null;
        }

        this.Cell = cell;
        this.Cell.Tile = this;

        // Запускаем анимацию перемещения
        StartCoroutine(Animate(cell.transform.position, false));
    }
    
    // Объединяет эту плитку с плиткой в указанной ячейке
    public void Merge(TileCell cell)
    {
        // Освобождаем текущую ячейку
        if (this.Cell != null)
        {
            this.Cell.Tile = null;
        }
        this.Cell = null;
        
        // Блокируем целевую плитку от повторного слияния
        cell.Tile.Locked = true;

        // Запускаем анимацию слияния (плитка будет уничтожена после анимации)
        StartCoroutine(Animate(cell.transform.position, true));
    }
    
    // Корутина для анимации перемещения плитки
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

        // Уничтожение плитки после слияния
        if (merging)
        {
            Destroy(gameObject);
        }
    }
}
