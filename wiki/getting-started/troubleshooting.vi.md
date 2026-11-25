---
title: Xử lý sự cố lần đầu
description: Chẩn đoán các lỗi PSE thường gặp ở lần chạy đầu mà không phải sửa sản phẩm sinh ra hay phần bên trong khung.
---

# Xử lý sự cố lần đầu

Bắt đầu từ tầng thất bại sớm nhất. Đổi nhiều thứ một lúc làm việc chẩn đoán khó hơn.

## Không tìm thấy `pse`

Bộ khởi động PSE không có sẵn trong shell hiện hành. Chạy lại lộ trình cài đặt bạn đã chọn, mở một terminal mới nếu PATH đã đổi, rồi chạy:

```text
pse doctor
```

## `pse doctor` báo thiếu LuaLaTeX

Hãy cài đặt hoặc sửa chữa một bản phân phối TeX có LuaLaTeX. Các bootstrap script của PSE cài PSE chứ không cài TeX.

## `pse doctor --deep` thất bại

Hãy coi các lỗi doctor bắt buộc là vấn đề máy trạm/môi trường trước khi gỡ lỗi cuốn sách. Sửa vấn đề Python, LuaLaTeX, gói TeX, phông cơ sở, ghi tạm hay safe-build được báo, rồi chạy lại doctor.

## `pse build .` nói dự án không hợp lệ

Xác nhận terminal của bạn đang ở thư mục gốc dự án được sinh ra, tức thư mục chứa `book.yml` và `main.tex`. Nếu bạn đã sửa `book.yml`, kiểm tra thụt lề YAML và các giá trị bắt buộc.

## LuaLaTeX lỗi sau một lần sửa nội dung

Hoàn tác hoặc cô lập lần sửa gần nhất. Kiểm tra ngoặc và chính tả lệnh trước. Tạo lại sau một sửa nhỏ thay vì thay đổi bố cục diện rộng.

## PDF tạo được nhưng trông sai

Chạy `pse check . --human`, rồi soát PDF. Nếu vấn đề là một ngoại lệ trình bày cho một đầu sách, `config/pse-local.tex` là điểm tùy biến cục bộ dự án dự kiến. Đừng vá các tệp lõi dùng chung để sửa một cuốn sách.

## Đặt lại sản phẩm sinh ra

Nội dung `build/` được sinh ra không phải nguồn chuẩn. Dùng quy trình của PSE thay vì sửa tay các tệp sinh ra. Giữ nguyên `book.yml`, `main.tex`, `content/`, `assets/` và cấu hình thuộc về dự án.

Nếu một bản khởi đầu tổng hợp tối giản cũng thất bại trong cùng môi trường, hãy tái hiện vấn đề bằng nội dung tổng hợp trước khi đưa một bản thảo riêng tư vào.

Tiếp: [Bước tiếp theo](next-steps.md).
