---
title: Mô hình chất lượng
description: Diễn giải các phát hiện máy của PSE mà không biến tự động hóa thành vật thay thế cho phán đoán biên tập.
---

# Mô hình chất lượng

Chạy QA dự án bằng:

```text
pse check . --human
```

Các phát hiện của PSE dùng bốn cấp nghiêm trọng:

| Nghiêm trọng | Ý nghĩa | Hành động bình thường |
| --- | --- | --- |
| `error` | vấn đề kỹ thuật/hợp đồng cản trở | sửa trước khi phát hành |
| `warning` | vấn đề kỹ thuật không cản trở | điều tra và xử lý hoặc ghi nhận |
| `review` | máy xác định được tình huống nhưng không ra phán đoán xuất bản | đọc soát bởi con người |
| `info` | trạng thái hoặc bằng chứng được ghi nhận | giữ làm ngữ cảnh |

Một lệnh trả về thành công không có nghĩa "không lỗi". QA máy là một tầng trong một quy trình biên tập và sản xuất lớn hơn.

## QA máy giỏi việc gì

Tùy hồ sơ/mô-đun đang hoạt động, QA có thể kiểm định siêu dữ liệu được khai báo, ID và quan hệ ngữ nghĩa, cấu trúc định vị, tham chiếu khảo chú, hợp đồng tệp sinh, kết quả biên dịch, hình học PDF và các bất biến kiểm tra máy khác.

## Những gì vẫn thuộc con người

Con người vẫn chịu trách nhiệm về những việc như độ chính xác sự thật, đối chiếu văn bản, chất lượng bản dịch, diễn giải học thuật, tính đúng của thư mục ngoài cấu trúc kiểm tra máy được, tính phù hợp của hình ảnh, cân bằng thị giác, thứ tự đọc như người dùng trải nghiệm, quyền pháp lý và phê duyệt xuất bản cuối.

Hãy dùng [Đọc soát bởi con người](../workflows/human-review.md) như một phần của vòng lặp sản xuất thay vì chỉ ở cuối.
