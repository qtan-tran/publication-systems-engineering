---
title: Kiểm định đầu ra
description: Soát siêu dữ liệu, điều hướng và khả năng trích xuất văn bản của PDF hoàn thành mà không đưa ra các khẳng định tiếp cận không có căn cứ.
---

# Kiểm định đầu ra

Soát trực tiếp một PDF đã tạo:

```text
pse inspect-output build/book.pdf --expected-language en --human
```

hoặc trỏ lệnh vào một thư mục dự án:

```text
pse inspect-output . --expected-language en
```

Đường cơ sở hiện hành kiểm tra khả năng đọc PDF, siêu dữ liệu tên sách/tác giả liên quan, ngôn ngữ tài liệu, dấu trang/điều hướng và khả năng trích xuất văn bản. Một báo cáo JSON có thể được ghi bằng `--output`.

## Những gì kiểm định đầu ra không chứng nhận

PSE hiện không chứng nhận cấu trúc tagged-PDF, thứ tự đọc, văn bản thay thế cho hình ảnh, PDF/UA, WCAG, tương thích lưu trữ hay tuân thủ tiếp cận về pháp lý. Những điều đó vẫn là các tầng soát xét/tương thích tường minh ngoài đường cơ sở tự động hiện tại.

## Sự gắn với phát hành

Với các bản phát hành schema hiện hành `0.2`, `pse release` chạy đường cơ sở soát đầu ra đối với PDF xuất bản cuối và lưu `output-inspection.json` trong thư mục phát hành. Bảng kê phát hành ghi mã băm của tệp soát và mã SHA-256 chính xác của PDF cuối mà bản soát áp dụng.

`pse verify-release` kiểm tra lại sự gắn ấy, nên việc thay PDF nhưng giữ một báo cáo soát cũ có thể bị phát hiện.
