using UnityEngine;

// Управляет сеткой ячеек игровой доски и предоставляет методы для работы с ячейками
public class TileGrid : MonoBehaviour
{
    public TileRow[] Rows { get; private set; }
    public TileCell[] Cells { get; private set; }

    public int Size => Cells.Length;
    public int Height => Rows.Length;
    public int Width => Size / Height;

    // Инициализация компонентов и установка координат ячеек
    private void Awake()
    {
        Rows = GetComponentsInChildren<TileRow>();
        Cells = GetComponentsInChildren<TileCell>();

        // Устанавливаем координаты ячеек на основе их индекса
        for (int i = 0; i < Cells.Length; i++)
        {
            Cells[i].Coordinates = new Vector2Int(i % Width, i / Width);
        }
    }

    // Дополнительная инициализация координат через структуру строк
    private void Start()
    {
        // Устанавливаем координаты через структуру строк для надежности
        for (int y = 0; y < Rows.Length; y++)
        {
            for (int x = 0; x < Rows[y].Cells.Length; x++)
            {
                Rows[y].Cells[x].Coordinates = new Vector2Int(x, y);
            }
        }
    }
    
    // Получает ячейку по координатам x и y
    public TileCell GetCell(int x, int y)
    {
        if (x >= 0 && x < Width && y >= 0 && y < Height)
        {
            return Rows[y].Cells[x];
        }
        else
        {
            return null;
        }
    }
    
    // Получает ячейку по координатам Vector2Int
    public TileCell GetCell(Vector2Int coordinates)
    {
        return GetCell(coordinates.x,coordinates.y);
    }
    
    // Получает соседнюю ячейку относительно указанной в заданном направлении
    public TileCell GetAdjacentCell(TileCell cell, Vector2Int direction)
    {
        Vector2Int coordinates = cell.Coordinates;
        coordinates.x += direction.x;
        coordinates.y -= direction.y; // Инвертируем Y, так как в Unity Y растет вверх

        return GetCell(coordinates);
    }
    
    // Находит случайную пустую ячейку на сетке
    public TileCell GetRandomEmptyCell()
    {
        // Начинаем со случайного индекса
        int index = Random.Range(0, Cells.Length);
        int startingIndex = index;

        // Ищем первую пустую ячейку, начиная со случайной позиции
        while (Cells[index].Occupied)
        {
            index++;

            // Переходим к началу массива, если достигли конца
            if (index >= Cells.Length)
            {
                index = 0;
            }

            // Если вернулись к начальной позиции, значит все ячейки заняты
            if (index == startingIndex)
            {
                return null;
            }
        }

        return Cells[index];
    }
}
