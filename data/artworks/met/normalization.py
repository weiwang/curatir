import json
def normalization(artwork):
    if artwork:
        artwork['artist'] = artwork['artist'].replace("Attributed to Goya (Francisco de Goya y Lucientes)", "Francisco Goya")
        artwork['artist'] = artwork['artist'].replace("Goya (Francisco de Goya y Lucientes)", "Francisco Goya")
        artwork['artist'] = artwork['artist'].replace("El Greco (Domenikos Theotokopoulos)", "El Greco")
        artwork['artist'] = artwork['artist'].replace("El Greco (Domenikos Theotokopoulos) and Workshop", "El Greco")      
        artwork['artist'] = artwork['artist'].replace("Jacques Louis David", "Jacques-Louis David")
        artwork['artist'] = artwork['artist'].replace("Vel\u00e1zquez (Diego Rodr\u00edguez de Silva y Vel\u00e1zquez)", "Diego Vel\u00e1zquez")
        artwork['artist'] = artwork['artist'].replace("Raphael (Raffaello Sanzio or Santi)", "Raphael")
        artwork['artist'] = artwork['artist'].replace("Titian (Tiziano Vecellio)", "Titian")
        artwork['artist'] = artwork['artist'].replace('Caravaggio (Michelangelo Merisi)', 'Caravaggio')
        artwork['artist'] = artwork['artist'].replace("Rembrandt (Rembrandt van Rijn)", "Rembrandt")
        artwork['artist'] = artwork['artist'].replace('Fra Angelico (Guido di Pietro)', 'Fra Angelico')
        artwork['artist'] = artwork['artist'].replace("Botticelli (Alessandro di Mariano Filipepi)", 'Botticelli')
        artwork['artist'] = artwork['artist'].replace("Paolo Uccello (Paolo di Dono)", "Paolo Uccello")
        artwork['artist'] = artwork['artist'].replace("Giotto di Bondone", "Giotto")
        artwork['artist'] = artwork['artist'].replace("Duccio di Buoninsegna", "Duccio")
        artwork['artist'] = artwork['artist'].replace("Pierre-Pierre-Pierre-Pierre-Auguste Renoir", "Pierre-Auguste Renoir")
        artwork['artist'] = artwork['artist'].replace("Camille Corot", "Jean-Baptiste-Camille Corot")
        artwork['artist'] = artwork['artist'].replace("Jacopo Tintoretto (Jacopo Robusti)", "Tintoretto")
    return artwork

met = json.load(open("met_painting_dump.json"))
met = map(normalization, met)
json.dump(met, open("met_painting_dump.json", 'wb'))
