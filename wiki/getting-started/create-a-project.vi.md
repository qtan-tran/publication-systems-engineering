---
title: Tạo dự án đầu tiên
description: Sinh một dự án sách PSE tổng hợp an toàn theo mặc định mà không phải sửa các tệp của khung.
---

# Tạo dự án đầu tiên

Tạo dự án trong **bộ nhớ riêng tư**, ngoài kho PSE công khai. Lệnh tương tác sẽ hỏi siêu dữ liệu sách cần thiết:

```text
pse new /path/to/private-projects --profile academic-monograph
```

Bạn sẽ được hỏi tên sách, tác giả/biên tập viên, ngôn ngữ, năm xuất bản và siêu dữ liệu tùy chọn. PSE sau đó in ra đúng thư mục nó đã tạo.

Để có một kiểm tra tổng hợp tái tạo được mà không cần gõ lần lượt, bạn có thể dùng:

```text
pse new /path/to/private-projects \
  --profile academic-monograph \
  --title "My First PSE Book" \
  --author "Example Author" \
  --language en \
  --publication-year 2026 \
  --non-interactive
```

Trên PowerShell, hãy nhập lệnh trên một dòng hoặc dùng cú pháp nối dòng của PowerShell thay cho dấu gạch chéo như trên.

Tên thư mục được sinh ra một cách an toàn từ tên sách trừ khi bạn cung cấp `--slug`. Đừng tạo dự án bằng cách sao chép phần bên trong của khung hoặc các gói hồ sơ.

Chuyển vào thư mục đã sinh trước khi tiếp tục phần còn lại của cẩm nang.

Tiếp: [Hiểu thư mục dự án](project-folder.md).
