# Vorbereitung-audiovisueller-Simulationsmodelle-in-der-Stadtplanung

Folgende Skripte können mit Hilfe des Pythoninterpreters in Blender ausgeführt werden.

Zellkomplexe mit Topologic:
    - Es kombiniert Mesh-Objekte zu einem einzigen Mesh (einem Zellkomplex)
    - Es bereinigt und vereinfacht das Mesh durch das Verschmelzen von Dreiecken
    - Es filtert bestimmte Flächen basierend auf ihrer Ausrichtung und Position
    - Es gruppiert Objekte nach ihren Elternobjekten
    - Es bearbeitet die Gruppen von Objekten, um den Workflow zu optimieren

  Materialien gruppieren:
    - Es geht alle vorhandenen Materialien durch und gruppiert Materialien mit ähnlichen Namen (z.B. "Timber01" und "Timber02")
    - Alle ähnlichen Materialien werden zu einem gemeinsamen Material zusammengefügt

    Materialien löschen:
      - Nicht (mehr) genutzte Materialien werden entfernt
