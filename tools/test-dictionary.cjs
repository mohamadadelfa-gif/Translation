const fs = require('node:fs');
const zlib = require('node:zlib');
const crypto = require('node:crypto');
const path = require('node:path');
const projectRoot = path.resolve(__dirname, '..');
const source = 'C:/Users/Adel/Desktop/Ariyan Pour Dictionary/Generic English-Persian Dictionary.ld2';
const bytes = fs.readFileSync(source);
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const initialHash = hash(bytes);
const u32 = p => bytes.readUInt32LE(p);
let start = u32(0x5c) + 0x60;
const type = u32(start);
if (type !== 3) start = start + 12 + u32(start + 4);
const end = start + 8 + u32(start + 4);
const header = start + 28 + u32(start + 8);
const indexLength = u32(start + 12);
const wordsLength = u32(start + 16);
const definitionsLength = u32(start + 20);
console.log(JSON.stringify({version: `${bytes.readUInt16LE(24)}.${bytes.readUInt16LE(26)}`,type,start,end,header,indexLength,wordsLength,definitionsLength}));
if (end > bytes.length || header >= end || indexLength % 10) throw Error('Unexpected dictionary layout');
let pos = header + 12;
let relative = u32(header + 8);
const offsets = [];
while (relative + pos < end) {
  const offset = u32(pos); pos += 4;
  if (!offset) throw Error('Unexpected zero compression offset');
  offsets.push(offset);
  relative = offset;
}
let previous = 0;
const chunks = offsets.map(offset => {
  if (offset <= previous || pos + offset > end) throw Error('Invalid compressed block bounds');
  const result = zlib.inflateSync(bytes.subarray(pos + previous, pos + offset), {maxOutputLength: 128*1024*1024});
  previous = offset;
  return result;
});
const data = Buffer.concat(chunks);
if (data.length !== indexLength + wordsLength + definitionsLength) throw Error('Uncompressed size mismatch');
const count = indexLength / 10 - 1;
const xmlBase = indexLength + wordsLength;
const records = [];
for (let i=0;i<count;i++) {
  const p=i*10;
  let w=data.readUInt32LE(p);
  const x=data.readUInt32LE(p+4), nextW=data.readUInt32LE(p+10), nextX=data.readUInt32LE(p+14);
  const refs=data[p+9];
  if (w>nextW || nextW>wordsLength || x>nextX || nextX>definitionsLength || w+refs*4>nextW) throw Error(`Bad entry offsets: ${i}`);
  const defs=[data.subarray(xmlBase+x,xmlBase+nextX)];
  for(let r=0;r<refs;r++) {
    const target=data.readUInt32LE(indexLength+w); w+=4;
    if(target>=count) throw Error('Invalid cross-reference');
    const a=data.readUInt32LE(target*10+4), b=data.readUInt32LE(target*10+14);
    if(a>b || b>definitionsLength) throw Error('Invalid referenced definition');
    defs.push(data.subarray(xmlBase+a,xmlBase+b));
  }
  records.push({wordBytes:data.subarray(indexLength+w,indexLength+nextW), definitionBytes:Buffer.concat(defs)});
}
const decoders = ['utf-8','utf-16le','utf-16be'];
for(const encoding of decoders) {
  const decoder=new TextDecoder(encoding,{fatal:true});
  let valid=0;
  for(const r of records.slice(0,100)) { try { decoder.decode(r.definitionBytes); valid++; } catch {} }
  console.log(JSON.stringify({encoding,validOf100:valid,preview: valid ? new TextDecoder(encoding).decode(records[50].definitionBytes).slice(0,220) : null}));
}
const wordDecoder = new TextDecoder('utf-8',{fatal:true});
const defDecoder = new TextDecoder('utf-8',{fatal:true});
const decoded = records.map((r,i)=>({index:i,word:wordDecoder.decode(r.wordBytes),definition:defDecoder.decode(r.definitionBytes)}));
const sourceByteRoundTrip = decoded.every((r,i)=>Buffer.from(r.word,'utf8').equals(records[i].wordBytes) && Buffer.from(r.definition,'utf8').equals(records[i].definitionBytes));
if (!sourceByteRoundTrip) throw Error('Source byte round-trip mismatch');
const persianCount = decoded.filter(r=>/[\u0600-\u06ff]/u.test(r.definition)).length;
const replacementCount = decoded.filter(r=>r.word.includes('\ufffd')||r.definition.includes('\ufffd')).length;
console.log(JSON.stringify({persianCount,replacementCount,affected:decoded.filter(r=>r.word.includes('\ufffd')||r.definition.includes('\ufffd')).slice(0,6)}));
if(persianCount < count/2) throw Error('Decoded content needs further encoding investigation');
const selected = new Set([0,1,2,Math.floor(count/4),Math.floor(count/2),Math.floor(count*3/4),count-1]);
const terms = new Set(['memory','guilt','restoration','autonomy','culture','history','responsibility','democracy']);
decoded.forEach((r,i)=>{if(terms.has(r.word.toLowerCase())) selected.add(i);});
const samples=[...selected].sort((a,b)=>a-b).map(i=>decoded[i]);
const outDir=path.join(projectRoot,'archive','dictionary-test'); fs.mkdirSync(outDir,{recursive:true});
const sample=samples.map(r=>`ENTRY ${r.index+1}: ${r.word}\n${r.definition}`).join('\n\n');
const samplePath=path.join(outDir,'utf8-sample.txt');
fs.writeFileSync(samplePath,sample,'utf8');
const plainSample=samples.map(r=>`${r.word}\n${r.definition.replace(/<[^>]*>/gu,'')}`).join('\n\n');
fs.writeFileSync(path.join(outDir,'readable-utf8-sample.txt'),plainSample,'utf8');
fs.writeFileSync(path.join(outDir,'source-character-issues.json'),JSON.stringify(decoded.filter(r=>r.word.includes('\ufffd')||r.definition.includes('\ufffd')),null,2),'utf8');
const reread=new TextDecoder('utf-8',{fatal:true}).decode(fs.readFileSync(samplePath));
if(reread!==sample) throw Error('UTF-8 sample round-trip failure');
// Verify every decoded entry can be encoded and decoded in UTF-8 without loss.
for(const r of decoded) for(const value of [r.word,r.definition]) {
  if(new TextDecoder('utf-8',{fatal:true}).decode(Buffer.from(value,'utf8'))!==value) throw Error('UTF-8 round-trip failure');
}
const report={source,sourceBytes:bytes.length,sourceSha256:initialHash,entries:count,compressedBlocks:chunks.length,uncompressedBytes:data.length,wordEncoding:'UTF-8',definitionEncoding:'UTF-8',entriesWithPersianArabicCharacters:persianCount,entriesWithReplacementCharacters:replacementCount,allEntriesStrictlyDecoded:true,allEntriesUtf8RoundTripPassed:true,sampleEntries:samples.length,sourceUnchanged:hash(fs.readFileSync(source))===initialHash,scope:'All entries validated in memory; only sample entries exported. Definition markup preserved; dictionary accuracy and attribution not independently verified.',formatReference:'https://github.com/nviet/lingoes-converter/blob/master/LingoesConverter.php'};
report.sourceByteRoundTripPassed=sourceByteRoundTrip;
report.characterIssueExplanation='Three entries contain literal U+FFFD replacement characters already present in the decompressed source bytes: apostle, asafetida, asafoetida. Extraction introduced no replacement characters.';
fs.writeFileSync(path.join(outDir,'test-report.json'),JSON.stringify(report,null,2),'utf8');
console.log(JSON.stringify(report,null,2));
console.log(sample);
if (process.argv.includes('--export-full')) {
  const glossaryDir=path.join(projectRoot,'translation-references','aryanpour');
  fs.mkdirSync(glossaryDir,{recursive:true});
  const plain = value => value.replace(/<n\s*\/>/giu,'\n').replace(/<[^>]*>/gu,'');
  const entries=decoded.map(r=>({id:r.index+1,english:r.word,persian:plain(r.definition),original_definition_markup:r.definition,source_character_issue:r.definition.includes('\ufffd')||r.word.includes('\ufffd')}));
  const jsonl=entries.map(r=>JSON.stringify(r)).join('\n')+'\n';
  const txt='Ariyanpour English–Persian Glossary\nSource: Generic English-Persian Dictionary.ld2\nAttribution supplied by the user; edition not independently verified.\n50,259 entries. Original wording and spelling retained.\nThree pre-existing damaged entries are listed in source-character-issues.json.\n\n'+entries.map(r=>`[${r.id}] ${r.english}\n${r.persian}`).join('\n\n')+'\n';
  fs.writeFileSync(path.join(glossaryDir,'aryanpour-english-persian.txt'),txt,'utf8');
  fs.writeFileSync(path.join(glossaryDir,'aryanpour-english-persian.jsonl'),jsonl,'utf8');
  fs.writeFileSync(path.join(glossaryDir,'source-character-issues.json'),JSON.stringify(entries.filter(r=>r.source_character_issue),null,2),'utf8');
  const verified = fs.readFileSync(path.join(glossaryDir,'aryanpour-english-persian.jsonl'),'utf8').trimEnd().split('\n').map(s=>JSON.parse(s));
  if(verified.length!==count || verified.some((r,i)=>r.english!==decoded[i].word||r.original_definition_markup!==decoded[i].definition)) throw Error('Full export verification failed');
  if(new TextDecoder('utf-8',{fatal:true}).decode(fs.readFileSync(path.join(glossaryDir,'aryanpour-english-persian.txt')))!==txt) throw Error('Text export verification failed');
  const exportReport={...report,scope:'Full glossary exported as readable UTF-8 text and JSON Lines with original definition markup preserved.',exportedEntries:verified.length,exportVerificationPassed:true,sourceUnchanged:hash(fs.readFileSync(source))===initialHash};
  fs.writeFileSync(path.join(glossaryDir,'conversion-report.json'),JSON.stringify(exportReport,null,2),'utf8');
  console.log(JSON.stringify({outputDirectory:glossaryDir,entries:verified.length,verificationPassed:true,files:fs.readdirSync(glossaryDir)},null,2));
}
