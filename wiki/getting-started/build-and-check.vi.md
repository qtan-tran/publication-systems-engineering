---
title: Tạo lập và kiểm tra PDF
description: Tạo một PDF hoạt động và chạy các kiểm tra máy của PSE trước khi làm bản đọc soát hay phát hành.
---

# Tạo lập và kiểm tra PDF

Từ thư mục gốc dự án, chạy:

```text
pse build .
pse check . --human
```

Một lần tạo lập thành công ghi PDF hoạt động vào:

```text
build/book.pdf
```

Hãy mở PDF ấy và soát bằng mắt. Các kiểm tra máy không thể quyết mọi câu hỏi biên tập hay thiết kế chữ.

## Đọc kết quả kiểm tra

PSE dùng cấp phát hiện:

| Cấp | Ý nghĩa |
| --- | --- |
| `error` | vấn đề cản trở |
| `warning` | cảnh báo kỹ thuật cần được chú ý |
| `review` | cần phán đoán biên tập/sản xuất của con người |
| `info` | trạng thái hay bằng chứng được ghi nhận |

Đừng diễn giải "PDF mở được" thành "cuốn sách đã sẵn sàng để xuất bản". Một bản tạo lập làm việc là một sản phẩm của quá trình lặp lại.

## Một vòng lặp đầu hữu ích

Dùng chu kỳ ngắn này khi biên tập:

```text
sửa nguồn → pse build . → pse check . --human → soát build/book.pdf
```

Khi một lệnh thất bại, đừng sửa các tệp được sinh trong `build/` để che biểu hiện. Hãy sửa nguồn hoặc cấu hình dự án đã sinh ra nó.

Tiếp: [Xử lý sự cố lần đầu](troubleshooting.md), hoặc, nếu mọi thứ chạy tốt, [Bước tiếp theo](next-steps.md).
