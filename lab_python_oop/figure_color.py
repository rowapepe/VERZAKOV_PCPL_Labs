class FigureColor:
    def __init__(self, color):
        self._color = color
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if isinstance(value, str) and value.strip():
            self._color = value.strip()
        else:
            raise ValueError("Цвет должен быть непустой строкой")
    
    def __init__(self, color):
        if isinstance(color, str) and color.strip():
            self._color = color.strip()
        else:
            raise ValueError("Цвет должен быть непустой строкой")
    
    def __str__(self):
        return self._color
