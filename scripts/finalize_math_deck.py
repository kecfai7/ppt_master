import io
import re
import zipfile

with open('수학.pptx', 'rb') as f:
    data = f.read()

in_zip = zipfile.ZipFile(io.BytesIO(data), 'r')
out_buf = io.BytesIO()
out_zip = zipfile.ZipFile(out_buf, 'w', compression=zipfile.ZIP_DEFLATED)

for item in in_zip.infolist():
    content = in_zip.read(item.filename)
    
    # 1. Update presentation.xml
    if item.filename == 'ppt/presentation.xml':
        text = content.decode('utf-8')
        # Ensure 16x9 screen type
        text = text.replace('type="screen4x3"', 'type="screen16x9"')
        # Ensure clean showPr without automatic timings
        if '<p:showPr' not in text:
            text = text.replace('</p:presentation>', '  <p:showPr/>\n</p:presentation>')
        else:
            text = re.sub(r'<p:showPr\b[^>]*>', '<p:showPr/>', text)
        content = text.encode('utf-8')
        
    # 2. Update slides: clean fade transition with advClick="1"
    elif item.filename.startswith('ppt/slides/slide') and item.filename.endswith('.xml'):
        text = content.decode('utf-8')
        text = re.sub(r'<p:transition\b.*?</p:transition>', '', text, flags=re.DOTALL)
        trans_xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" advClick="1"><p:fade dur="300"/></p:transition>'
        text = text.replace('</p:sld>', f'  {trans_xml}\n</p:sld>')
        content = text.encode('utf-8')
        
    out_zip.writestr(item, content)

out_zip.close()
in_zip.close()

with open('수학.pptx', 'wb') as f:
    f.write(out_buf.getvalue())

print("Cleaned up 수학.pptx transitions and 16:9 presentation properties successfully!")

