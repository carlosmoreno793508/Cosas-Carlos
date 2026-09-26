const pptxgen = require('pptxgenjs');
const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';           // 13.3 x 7.5
const W=13.3, H=7.5;

const INK='1B1B1F', INK2='26262B', CARDL='EDEDF0', PAPER='FFFFFF';
const GOLD='C6972F', GOLDL='E3C878', SILVER='A9AEB5', MUTED='6B6B72', WHITE='FFFFFF';
const HF='Cambria', BF='Calibri';

function sh(){return {type:'outer', color:'000000', opacity:0.28, blur:8, offset:3, angle:90};}
function monogram(s,x,y,size){
  s.addShape(p.ShapeType.roundRect,{x,y,w:size,h:size,rectRadius:size*0.18,fill:{color:GOLD},shadow:sh()});
  s.addText('TID',{x,y,w:size,h:size,align:'center',valign:'middle',fontFace:HF,bold:true,color:INK,fontSize:size*18});
}

/* ---------- Slide 1 — Cover (dark) ---------- */
let s=p.addSlide(); s.background={color:INK};
monogram(s,0.9,0.85,1.0);
s.addText('Decoración Industrial',{x:0.9,y:2.5,w:11,h:1.1,fontFace:HF,bold:true,color:WHITE,fontSize:52,margin:0});
s.addText('Foil, tintas y acabados — con abasto local, sin depender de importar.',
  {x:0.92,y:3.7,w:10.5,h:0.8,fontFace:BF,color:GOLDL,fontSize:21,margin:0});
s.addShape(p.ShapeType.line,{x:0.95,y:4.75,w:3.6,h:0,line:{color:GOLD,width:2}});
s.addText('México  ·  Centroamérica  ·  EE.UU.',{x:0.9,y:6.35,w:7,h:0.4,fontFace:BF,color:SILVER,fontSize:14,margin:0});
s.addText('www.tidmexico.com.mx',{x:6.3,y:6.35,w:6.1,h:0.4,align:'right',fontFace:BF,bold:true,color:WHITE,fontSize:14,margin:0});

/* ---------- Slide 2 — Problem/solution (light) ---------- */
s=p.addSlide(); s.background={color:PAPER};
s.addText('Deja de depender de importar',{x:0.9,y:0.6,w:11.5,h:0.9,fontFace:HF,bold:true,color:INK,fontSize:38,margin:0});
s.addText('Traer foil y tintas de lejos te cuesta tiempo, dinero y paros de línea. TID te da la misma calidad, aquí.',
  {x:0.92,y:1.5,w:11.4,h:0.6,fontFace:BF,color:MUTED,fontSize:17,margin:0});
// card A
s.addShape(p.ShapeType.roundRect,{x:0.9,y:2.5,w:5.6,h:4.1,rectRadius:0.14,fill:{color:CARDL},shadow:sh()});
s.addText('Importar foil y tintas',{x:1.2,y:2.8,w:5,h:0.5,fontFace:HF,bold:true,color:INK,fontSize:20,margin:0});
s.addText([
 {text:'Lead times largos e inciertos',options:{bullet:{code:'2022'},breakLine:true}},
 {text:'Costos y logística altos',options:{bullet:{code:'2022'},breakLine:true}},
 {text:'Sin soporte técnico local',options:{bullet:{code:'2022'},breakLine:true}},
 {text:'Riesgo de parar la línea',options:{bullet:{code:'2022'},breakLine:false}},
],{x:1.2,y:3.5,w:5.05,h:2.8,fontFace:BF,color:'44444A',fontSize:16,paraSpaceAfter:12,margin:0});
// card B (gold tint)
s.addShape(p.ShapeType.roundRect,{x:6.8,y:2.5,w:5.6,h:4.1,rectRadius:0.14,fill:{color:'FBF4E6'},line:{color:GOLD,width:1},shadow:sh()});
s.addText('Con TID',{x:7.1,y:2.8,w:5,h:0.5,fontFace:HF,bold:true,color:'8A6A1E',fontSize:20,margin:0});
s.addText([
 {text:'Abasto local y rápido',options:{bullet:{code:'2713'},breakLine:true}},
 {text:'Segunda fuente confiable',options:{bullet:{code:'2713'},breakLine:true}},
 {text:'Muestras para validar',options:{bullet:{code:'2713'},breakLine:true}},
 {text:'Soporte técnico integral',options:{bullet:{code:'2713'},breakLine:false}},
],{x:7.1,y:3.5,w:5.05,h:2.8,fontFace:BF,color:'3D3320',fontSize:16,paraSpaceAfter:12,margin:0});

/* ---------- Slide 3 — Capabilities grid (light) ---------- */
s=p.addSlide(); s.background={color:PAPER};
s.addText('Todo para decorar, en un solo proveedor',{x:0.9,y:0.6,w:11.5,h:0.9,fontFace:HF,bold:true,color:INK,fontSize:34,margin:0});
const caps=[
 ['1','Hot Stamping Foil','Metálico, pigmento, brushed, chrome, hairline'],
 ['2','Tintas','Tampografía (pad) y serigrafía'],
 ['3','Color-Matching','Igualación exacta de color'],
 ['4','Labels','Etiquetas a la medida de tu proceso'],
 ['5','Dados & Fixtures','Herramentales, pads, rings, plates'],
 ['6','Soporte técnico','Desarrollo, capacitación y control de proceso'],
];
const gx=0.9, gy=1.75, cw=3.75, ch=2.45, gapx=0.28, gapy=0.28;
caps.forEach((c,i)=>{
  const col=i%3, row=Math.floor(i/3);
  const x=gx+col*(cw+gapx), y=gy+row*(ch+gapy);
  s.addShape(p.ShapeType.roundRect,{x,y,w:cw,h:ch,rectRadius:0.12,fill:{color:CARDL},shadow:sh()});
  s.addShape(p.ShapeType.ellipse,{x:x+0.3,y:y+0.32,w:0.7,h:0.7,fill:{color:GOLD}});
  s.addText(c[0],{x:x+0.3,y:y+0.32,w:0.7,h:0.7,align:'center',valign:'middle',fontFace:HF,bold:true,color:INK,fontSize:22,margin:0});
  s.addText(c[1],{x:x+0.3,y:y+1.2,w:cw-0.6,h:0.5,fontFace:HF,bold:true,color:INK,fontSize:18,margin:0});
  s.addText(c[2],{x:x+0.3,y:y+1.68,w:cw-0.6,h:0.6,fontFace:BF,color:MUTED,fontSize:13.5,margin:0});
});

/* ---------- Slide 4 — Foils (dark, star) ---------- */
s=p.addSlide(); s.background={color:INK};
s.addText([{text:'Hot Stamping ',options:{color:WHITE}},{text:'Foil',options:{color:GOLD}}],
  {x:0.9,y:0.6,w:11.5,h:0.9,fontFace:HF,bold:true,fontSize:36,margin:0});
s.addText('El acabado metálico de lujo que ninguna impresión directa iguala — aplicado en seco, a alta temperatura.',
  {x:0.92,y:1.5,w:11.4,h:0.6,fontFace:BF,color:SILVER,fontSize:15,margin:0});
const foils=[
 ['Metálico','Vapor-deposición de aluminio; brillo oro, azul, rosa y más'],
 ['Pigmento','Coating foil; efecto tipo serigrafía en seco'],
 ['Brushed','Aspecto de aluminio cepillado; líneas y colores variables'],
 ['Chrome','Efecto cromo espejo sobre plástico'],
 ['Hairline','Textura fina de líneas metálicas'],
 ['In-mold','Decoración integrada al molde'],
];
const fx=0.9, fy=2.35, fw=3.75, fh=1.85, fgx=0.28, fgy=0.28;
foils.forEach((c,i)=>{
  const col=i%3, row=Math.floor(i/3);
  const x=fx+col*(fw+fgx), y=fy+row*(fh+fgy);
  s.addShape(p.ShapeType.roundRect,{x,y,w:fw,h:fh,rectRadius:0.1,fill:{color:INK2}});
  s.addText(c[0],{x:x+0.28,y:y+0.22,w:fw-0.5,h:0.45,fontFace:HF,bold:true,color:GOLDL,fontSize:18,margin:0});
  s.addText(c[1],{x:x+0.28,y:y+0.7,w:fw-0.5,h:1.0,fontFace:BF,color:'C9CCD1',fontSize:13,margin:0});
});

/* ---------- Slide 5 — Industries (light) ---------- */
s=p.addSlide(); s.background={color:PAPER};
s.addText('Industrias que confían en TID',{x:0.9,y:0.6,w:11.5,h:0.9,fontFace:HF,bold:true,color:INK,fontSize:34,margin:0});
const inds=['Electrodomésticos','Automotriz','Médico','Cosmética','Industrial'];
const iw=2.2, igap=0.24, itot=inds.length*iw+(inds.length-1)*igap, ix0=(W-itot)/2;
inds.forEach((n,i)=>{
  const x=ix0+i*(iw+igap), y=2.1;
  s.addShape(p.ShapeType.roundRect,{x,y,w:iw,h:2.4,rectRadius:0.12,fill:{color:CARDL},shadow:sh()});
  s.addShape(p.ShapeType.ellipse,{x:x+iw/2-0.45,y:y+0.4,w:0.9,h:0.9,fill:{color:'FBF4E6'},line:{color:GOLD,width:1.5}});
  s.addText(String(i+1),{x:x+iw/2-0.45,y:y+0.4,w:0.9,h:0.9,align:'center',valign:'middle',fontFace:HF,bold:true,color:GOLD,fontSize:24,margin:0});
  s.addText(n,{x:x+0.1,y:y+1.5,w:iw-0.2,h:0.8,align:'center',fontFace:HF,bold:true,color:INK,fontSize:16,margin:0});
});
s.addShape(p.ShapeType.roundRect,{x:2.0,y:5.15,w:9.3,h:1.15,rectRadius:0.12,fill:{color:INK}});
s.addText('Proveedor single o secondary source en México, Centroamérica y EE.UU.',
  {x:2.2,y:5.15,w:8.9,h:1.15,align:'center',valign:'middle',fontFace:HF,italic:true,color:GOLDL,fontSize:19,margin:0});

/* ---------- Slide 6 — CTA + contacts (dark) ---------- */
s=p.addSlide(); s.background={color:INK};
s.addText('Pide tus muestras',{x:0.9,y:0.9,w:11.5,h:0.95,fontFace:HF,bold:true,color:WHITE,fontSize:44,margin:0});
s.addText('Validamos tu aplicación con muestras y te acompañamos en todo el proceso.',
  {x:0.92,y:1.95,w:11,h:0.6,fontFace:BF,color:SILVER,fontSize:17,margin:0});
const diffs=[['Abasto local','Entrega rápida en la región'],['Muestras','Prueba antes de comprometerte'],['Soporte integral','Desde el desarrollo hasta la producción']];
diffs.forEach((d,i)=>{
  const x=0.9+i*3.95, y=2.85;
  s.addShape(p.ShapeType.roundRect,{x,y,w:3.6,h:1.6,rectRadius:0.1,fill:{color:INK2}});
  s.addText(d[0],{x:x+0.25,y:y+0.22,w:3.1,h:0.5,fontFace:HF,bold:true,color:GOLDL,fontSize:18,margin:0});
  s.addText(d[1],{x:x+0.25,y:y+0.72,w:3.1,h:0.7,fontFace:BF,color:'C9CCD1',fontSize:13.5,margin:0});
});
s.addShape(p.ShapeType.line,{x:0.95,y:4.9,w:11.4,h:0,line:{color:'3A3A40',width:1}});
s.addText('Contáctanos',{x:0.9,y:5.05,w:6,h:0.4,fontFace:HF,bold:true,color:WHITE,fontSize:16,margin:0});
const contacts=[
 'Carlos Moreno   ·   +52 (868) 835 4777   ·   carlos.moreno@tidmexico.com.mx',
 'Arnulfo López   ·   +1 (708) 409-0288   ·   arnulfo.lopez@tidmexico.com.mx',
 'Jorge Galicia   ·   +52 (446) 479 4420   ·   jorge.galicia@tidmexico.com.mx',
];
s.addText(contacts.map((c,i)=>({text:c,options:{breakLine:true,color:'D7D9DD'}})),
  {x:0.9,y:5.5,w:11.5,h:1.2,fontFace:BF,fontSize:14,paraSpaceAfter:6,margin:0});
s.addText('www.tidmexico.com.mx',{x:0.9,y:6.9,w:11.5,h:0.4,fontFace:BF,bold:true,color:GOLD,fontSize:14,margin:0});

p.writeFile({fileName:'TID_Pitch_Corto.pptx'}).then(f=>console.log('OK',f));
