---
title: Hiểu thư mục dự án
description: Biết các tệp dự án PSE được sinh ra đâu là nguồn, cấu hình, tài nguyên và đâu là sản phẩm tạo lập dùng xong bỏ.
---

# Hiểu thư mục dự án

Một bản khởi đầu `academic-monograph` được sinh ra có hình dạng sau:

```text
my-first-pse-book/
├── book.yml
├── main.tex
├── content/
│   └── chapter-01.tex
├── assets/
├── config/
│   ├── pse-local.tex
│   └── semantic-modules.json
├── tests/
├── README.md
├── SECURITY.md
└── .gitignore
```

Sau một lần tạo lập, PSE tạo `build/`. **Đừng chỉnh các tệp trong `build/` như nguồn.** Chúng được sinh ra và có thể được tạo lại.

Các tệp bạn thường chạm tới trước tiên là:

- `book.yml` — siêu dữ liệu cấp đầu sách như tên, tác giả/biên tập viên, ngôn ngữ, năm, hồ sơ và khổ trang;
- `content/` — nguồn bản thảo;
- `main.tex` — thứ tự lắp ráp cuốn sách; người mới thường ít hoặc không cần đổi ở đây trong lần thử đầu;
- `assets/` — hình ảnh và tài nguyên thuộc về dự án;
- `config/pse-local.tex` — ngoại lệ trình bày cục bộ đầu sách có chừng mực;
- `config/semantic-modules.json` — kích hoạt tính năng ngữ nghĩa; hãy để nguyên cho tới khi bạn chắc chắn cần đổi.

Đừng sửa lõi dùng chung của PSE hay một hồ sơ đã cài đặt để tạo một ngoại lệ cho một cuốn sách. Ngoại lệ cục bộ đầu sách thuộc về trong dự án.

Tiếp: [Thay nội dung khởi đầu](edit-your-book.md).
