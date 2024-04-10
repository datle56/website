import os
import glob

# Định nghĩa đoạn mã Google Tag
google_tag = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-N786BFXKX9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-N786BFXKX9');
</script>
"""

# Thay đổi đường dẫn tới thư mục chứa các file HTML của bạn
folder_path = r'E:\WIKIPRJ\website\templates'

# Duyệt qua tất cả các file HTML trong thư mục
for html_file in glob.glob(os.path.join(folder_path, '*.html')):
    with open(html_file, 'r+' ,encoding='utf-8') as file:
        content = file.read()
        # Tìm vị trí của thẻ head và thêm Google Tag vào sau nó
        head_index = content.find('</head>')
        if head_index != -1:
            new_content = content[:head_index] + google_tag + content[head_index:]
            # Ghi lại nội dung mới vào file
            file.seek(0)
            file.write(new_content)
            file.truncate()
