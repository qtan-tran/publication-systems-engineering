---
title: Chỉnh sửa cuốn sách của bạn
description: Thay siêu dữ liệu và nội dung bản thảo khởi đầu tổng hợp của PSE mà vẫn giữ cấu trúc ngữ nghĩa.
---

# Thay nội dung khởi đầu

Trong vòng đầu tiên, chỉ nên sửa một chỗ nhỏ để vấn đề cài đặt và vấn đề bản thảo còn dễ phân biệt.

## Sửa siêu dữ liệu

Mở `book.yml`. Một bản khởi đầu cơ bản trông như sau:

```yaml
title: My First PSE Book
subtitle: ''
author: Example Author
language: en
publication_year: 2026
profile: academic-monograph
page:
  width_mm: 126
  height_mm: 198
```

Giữ nguyên thụt lề YAML. Đừng đổi tên hồ sơ một cách tùy tiện sau khi sinh dự án; các hồ sơ có thể có cấu trúc khởi đầu và yêu cầu ngữ nghĩa khác nhau.

## Sửa nội dung bản thảo

Mở `content/chapter-01.tex` và thay đoạn văn tổng hợp. Hãy giữ các lệnh ngữ nghĩa thay vì giả tạo hình thức của chúng bằng tay:

```tex
\chapter{First chapter}

This is the first paragraph of my test book.

\section{A first section}

This is another paragraph with a footnote.\footnote{A synthetic test note.}
```

Dùng các lệnh như `\chapter`, `\section`, trích dẫn, chú thích cuối trang, và các lệnh ngữ nghĩa riêng của hồ sơ để nói **một đoạn là gì**. Hãy để hồ sơ quyết định cấu trúc ấy trông thế nào.

!!! warning "Giữ nguồn ở trạng thái riêng tư"
    Sau khi qua giai đoạn kiểm tra tổng hợp, hãy giữ văn bản chưa xuất bản và tài nguyên dự án trong một kho riêng tư hoặc bộ nhớ riêng tư do bạn hoặc tổ chức của bạn kiểm soát. Đừng đặt bản thảo hay bản đọc soát cho người nhận vào kho PSE công khai.

Tiếp: [Tạo lập và kiểm tra PDF](build-and-check.md).
