using UnityEngine;

// ScriptableObject, определяющий визуальное состояние плитки (цвета для разных значений)
[CreateAssetMenu(menuName = "Tile State")]
public class TileState : ScriptableObject
{
    // Числовое значение, соответствующее этому состоянию (используется для идентификации)
    public int number;
    // Цвет фона плитки
    public Color backgroundColor;
    // Цвет текста на плитке
    public Color textColor;
}
