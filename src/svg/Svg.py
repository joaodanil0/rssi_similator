
import xml.etree.ElementTree as ET


class Svg:

    def __init__(self, svgFile) -> None:
        tree = ET.parse(svgFile)
        root = tree.getroot()
        g = self.getMainGTag(root)
        self.getInformations(g)

    def getMainGTag(self, root):
        for child in root:
            if child.tag == "{http://www.w3.org/2000/svg}g":
                return child
        return None
    
    def getInformations(self, root):
        beacons = {}
        points = {}
        for child in root:
            if self.hasLabel(child):   
                if self.isBeacon(child):            
                    info = self.getBeaconPosition(child)
                    beacons[info[0]] = info[1]
                elif self.isPoint(child):
                    info = self.getPointPosition(child)
                    points[info[0]] = info[1]
        # print(beacons)
        print(points.keys())

    def hasLabel(self, root):
        return "{http://www.inkscape.org/namespaces/inkscape}label" in root.attrib
    
    def isBeacon(self, root):
        return root.attrib["{http://www.inkscape.org/namespaces/inkscape}label"] == "beacon"
    
    def isPoint(self, root):
        return root.attrib["{http://www.inkscape.org/namespaces/inkscape}label"] == "point"

    def getBeaconPosition(self, root):        
        translate = self.getTranslate(root)
        position = {}
        for child in root:
            if self.isText(child):
                position["id"] = self.getId(child)
            elif self.isCircle(child):
                pos = self.getPos(child)
                finalPos = self.sumPos(translate, pos)
                position["pos"] = finalPos
        return position["id"], position["pos"]
    
    def getPointPosition(self, root):
        x = root.attrib["cx"]
        y = root.attrib["cy"]

        name = str(int(float(x))) + "_" + str(int(float(y)))
        pos = (float(x), float(y))
        return name, pos

    def isCircle(self, root):
        return root.tag == "{http://www.w3.org/2000/svg}circle"
    
    def getPos(self, root):
        return float(root.attrib["cx"]), float(root.attrib["cy"])
    
    def sumPos(self, pos1, pos2):
        return pos1[0] + pos2[0], pos1[1] + pos2[1] - 19.12
    
    def getTranslate(self, root):
        s = root.attrib["transform"]
        info = s[s.find("(")+1:s.find(")")]
        info = info.split(",")
        return float(info[0]), float(info[1])
    
    def isText(self, root):
        return root.tag == "{http://www.w3.org/2000/svg}text"
    
    def getId(sefl, root):
        for child in root:
            return child.text
