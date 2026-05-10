import xml.etree.ElementTree as ET
from xml.dom import minidom
import uuid

def generar_uml():
    clases = [
        {
            'id': 'Transaccion',
            'nombre': '«abstract»\nTransaccion',
            'atributos': [
                '- id: str',
                '- monto: float',
                '- descripcion: str',
                '- categoria: str',
                '- fecha: str'
            ],
            'metodos': [
                '+ registrar(): void {abstract}',
                '+ __str__(): str'
            ],
            'x': 420, 'y': 40,
            'color': '#dae8fc', 'stroke': '#6c8ebf'
        },
        {
            'id': 'Ingreso',
            'nombre': 'Ingreso',
            'atributos': ['- meta_id: str'],
            'metodos': [
                '+ registrar(): void',
                '+ __str__(): str'
            ],
            'x': 80, 'y': 360,
            'color': '#d5e8d4', 'stroke': '#82b366'
        },
        {
            'id': 'Gasto',
            'nombre': 'Gasto',
            'atributos': ['- meta_id: str'],
            'metodos': [
                '+ registrar(): void',
                '+ verificar_limite(limite: float): bool',
                '+ __str__(): str'
            ],
            'x': 420, 'y': 360,
            'color': '#d5e8d4', 'stroke': '#82b366'
        },
        {
            'id': 'Usuario',
            'nombre': 'Usuario',
            'atributos': [
                '- id: str',
                '- nombre: str',
                '- username: str',
                '- password: str',
                '- fecha_creacion: str'
            ],
            'metodos': [
                '+ autenticar(password: str): bool',
                '+ __str__(): str'
            ],
            'x': 820, 'y': 40,
            'color': '#fff2cc', 'stroke': '#d6b656'
        },
        {
            'id': 'Meta',
            'nombre': 'Meta',
            'atributos': [
                '- id: str',
                '- nombre: str',
                '- emoji: str',
                '- categoria: str',
                '- monto_objetivo: float',
                '- monto_actual: float',
                '- fecha_limite: str',
                '- completada: bool'
            ],
            'metodos': [
                '+ agregar_dinero(monto: float): void',
                '+ retirar_dinero(monto: float): void',
                '+ calcular_progreso(): float',
                '+ __str__(): str'
            ],
            'x': 820, 'y': 380,
            'color': '#fff2cc', 'stroke': '#d6b656'
        },
        {
            'id': 'TarjetaCredito',
            'nombre': 'TarjetaCredito',
            'atributos': [
                '- id: str',
                '- nombre: str',
                '- cupo_total: float',
                '- saldo_actual: float',
                '- pago_minimo: float',
                '- pago_total: float',
                '- dia_corte: int',
                '- dia_pago: int'
            ],
            'metodos': [
                '+ registrar_pago(monto: float): void',
                '+ calcular_disponible(): float',
                '+ calcular_uso(): float',
                '+ __str__(): str'
            ],
            'x': 1200, 'y': 40,
            'color': '#fff2cc', 'stroke': '#d6b656'
        },
        {
            'id': 'GestorPresupuesto',
            'nombre': 'GestorPresupuesto',
            'atributos': [
                '- limites: dict',
                '- ingresos_semanales: dict',
                '- categorias: list'
            ],
            'metodos': [
                '+ agregar_limite(cat: str, monto: float): void',
                '+ obtener_limite(cat: str): float',
                '+ agregar_categoria(nombre: str): void',
                '+ calcular_gasto_categoria(txns: list, cat: str): float'
            ],
            'x': 80, 'y': 700,
            'color': '#e1d5e7', 'stroke': '#9673a6'
        },
        {
            'id': 'GestorArchivos',
            'nombre': 'GestorArchivos',
            'atributos': ['- ruta_base: str'],
            'metodos': [
                '+ guardar_usuario(u: Usuario): void',
                '+ cargar_usuario(username: str): Usuario',
                '+ guardar_transacciones(t: list): void',
                '+ cargar_transacciones(): list',
                '+ guardar_metas(m: list): void',
                '+ cargar_metas(): list',
                '+ guardar_tarjetas(t: list): void',
                '+ cargar_tarjetas(): list'
            ],
            'x': 420, 'y': 700,
            'color': '#e1d5e7', 'stroke': '#9673a6'
        }
    ]

    relaciones = [
        ('Ingreso',         'Transaccion',      'endArrow=block;endFill=0;edgeStyle=orthogonalEdgeStyle;',          ''),
        ('Gasto',           'Transaccion',      'endArrow=block;endFill=0;edgeStyle=orthogonalEdgeStyle;',          ''),
        ('Usuario',         'Transaccion',      'endArrow=open;endFill=0;edgeStyle=orthogonalEdgeStyle;',           '1..*'),
        ('Usuario',         'Meta',             'endArrow=open;endFill=0;edgeStyle=orthogonalEdgeStyle;',           '1..*'),
        ('Usuario',         'TarjetaCredito',   'endArrow=open;endFill=0;edgeStyle=orthogonalEdgeStyle;',           '1..*'),
        ('Usuario',         'GestorPresupuesto','endArrow=open;endFill=0;edgeStyle=orthogonalEdgeStyle;',           '1'),
        ('GestorArchivos',  'Usuario',          'endArrow=open;dashed=1;edgeStyle=orthogonalEdgeStyle;',            ''),
        ('GestorArchivos',  'Transaccion',      'endArrow=open;dashed=1;edgeStyle=orthogonalEdgeStyle;',            ''),
        ('GestorArchivos',  'Meta',             'endArrow=open;dashed=1;edgeStyle=orthogonalEdgeStyle;',            ''),
        ('GestorArchivos',  'TarjetaCredito',   'endArrow=open;dashed=1;edgeStyle=orthogonalEdgeStyle;',            ''),
        ('Ingreso',         'Meta',             'endArrow=open;dashed=1;edgeStyle=orthogonalEdgeStyle;',            '0..1'),
        ('Gasto',           'Meta',             'endArrow=open;dashed=1;edgeStyle=orthogonalEdgeStyle;',            '0..1'),
    ]

    HEADER_H  = 40
    SEP_H     = 8
    ROW_H     = 26
    WIDTH     = 250

    root_el = ET.Element('mxfile')
    root_el.set('host', 'app.diagrams.net')

    diagram = ET.SubElement(root_el, 'diagram')
    diagram.set('name', 'PersonalBudgetManager UML')
    diagram.set('id', str(uuid.uuid4()))

    gm = ET.SubElement(diagram, 'mxGraphModel')
    for k, v in [('dx','1422'),('dy','762'),('grid','1'),('gridSize','10'),
                 ('guides','1'),('tooltips','1'),('connect','1'),('arrows','1'),
                 ('fold','1'),('page','1'),('pageScale','1'),
                 ('pageWidth','1900'),('pageHeight','1300'),('math','0'),('shadow','0')]:
        gm.set(k, v)

    root_cell = ET.SubElement(gm, 'root')
    ET.SubElement(root_cell, 'mxCell', id='0')
    ET.SubElement(root_cell, 'mxCell', id='1', parent='0')

    cell_id   = 2
    id_map    = {}

    for cls in clases:
        n_attr    = len(cls['atributos'])
        n_met     = len(cls['metodos'])
        total_h   = HEADER_H + SEP_H + n_attr * ROW_H + SEP_H + n_met * ROW_H + 10
        cid       = str(cell_id)
        id_map[cls['id']] = cid

        cc = ET.SubElement(root_cell, 'mxCell')
        cc.set('id', cid)
        cc.set('value', cls['nombre'])
        cc.set('style', (
            f"swimlane;fontStyle=1;align=center;verticalAlign=top;"
            f"childLayout=stackLayout;horizontal=1;startSize={HEADER_H};"
            f"horizontalStack=0;resizeParent=1;resizeParentMax=0;"
            f"collapsible=0;marginBottom=0;swimlaneHead=0;"
            f"fillColor={cls['color']};strokeColor={cls['stroke']};"
        ))
        cc.set('vertex', '1')
        cc.set('parent', '1')
        g = ET.SubElement(cc, 'mxGeometry')
        g.set('x', str(cls['x'])); g.set('y', str(cls['y']))
        g.set('width', str(WIDTH)); g.set('height', str(total_h))
        g.set('as', 'geometry')
        cell_id += 1; pid = cid

        def sep(y_pos):
            nonlocal cell_id
            s = ET.SubElement(root_cell, 'mxCell')
            s.set('id', str(cell_id)); s.set('value', '')
            s.set('style', f'line;strokeColor={cls["stroke"]};fillColor=none;')
            s.set('vertex', '1'); s.set('parent', pid)
            sg = ET.SubElement(s, 'mxGeometry')
            sg.set('y', str(y_pos)); sg.set('width', str(WIDTH))
            sg.set('height', str(SEP_H)); sg.set('as', 'geometry')
            cell_id += 1

        def row(text, y_pos):
            nonlocal cell_id
            r = ET.SubElement(root_cell, 'mxCell')
            r.set('id', str(cell_id)); r.set('value', text)
            r.set('style', (
                'text;strokeColor=none;fillColor=none;align=left;'
                'verticalAlign=top;spacingLeft=4;spacingRight=4;'
                'overflow=hidden;rotatable=0;'
                'points=[[0,0.5],[1,0.5]];portConstraint=eastwest;'
            ))
            r.set('vertex', '1'); r.set('parent', pid)
            rg = ET.SubElement(r, 'mxGeometry')
            rg.set('y', str(y_pos)); rg.set('width', str(WIDTH))
            rg.set('height', str(ROW_H)); rg.set('as', 'geometry')
            cell_id += 1

        cy = HEADER_H
        sep(cy); cy += SEP_H
        for a in cls['atributos']:
            row(a, cy); cy += ROW_H
        sep(cy); cy += SEP_H
        for m in cls['metodos']:
            row(m, cy); cy += ROW_H

    for src, tgt, style, label in relaciones:
        e = ET.SubElement(root_cell, 'mxCell')
        e.set('id', str(cell_id)); e.set('value', label)
        e.set('style', style); e.set('edge', '1')
        e.set('source', id_map[src]); e.set('target', id_map[tgt])
        e.set('parent', '1')
        eg = ET.SubElement(e, 'mxGeometry')
        eg.set('relative', '1'); eg.set('as', 'geometry')
        cell_id += 1

    xml_str  = ET.tostring(root_el, encoding='unicode')
    dom      = minidom.parseString(xml_str)
    pretty   = '\n'.join(dom.toprettyxml(indent='  ').split('\n')[1:])

    nombre_archivo = 'PersonalBudgetManager_UML.drawio'
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(pretty)

    print(f"✅  Archivo generado: {nombre_archivo}")
    print("📌  Importar en Lucidchart: File → Import → diagrams.net → sube el archivo")

if __name__ == '__main__':
    generar_uml()
