using UnityEngine;

// Представляет одну строку ячеек на игровой доске
public class TileRow : MonoBehaviour
{
    public TileCell[] Cells { get; private set; }

    // Инициализация ячеек строки при создании объекта
    private void Awake()
    {
        Cells = GetComponentsInChildren<TileCell>();
    }

}
