---
title: Chu trình sửa–tạo lập–kiểm tra hằng ngày
description: Dùng vòng lặp sản xuất an toàn ngắn nhất trong khi bản thảo và trình bày còn thay đổi.
---

# Chu trình sửa–tạo lập–kiểm tra hằng ngày

Trong công việc biên tập thông thường, dùng vòng lặp này:

```text
sửa nguồn chuẩn
      ↓
pse build .
      ↓
pse check . --human
      ↓
soát build/book.pdf
      ↓
sửa nguồn và lặp lại
```

`pse build .` tạo PDF hoạt động tại `build/book.pdf`. `pse check . --human` chạy QA máy đối với dự án mà không viết lại nguồn bản thảo.

## Những gì thuộc về nguồn

Hãy coi những thứ sau là nguồn sự thật chỉnh sửa được của dự án:

- `book.yml` — siêu dữ liệu ấn phẩm;
- `content/` — bản thảo và nội dung ấn phẩm có cấu trúc;
- `config/` — cấu hình dự án;
- `config/pse-local.tex` — các ghi đè trình bày cục bộ đầu sách được cho phép;
- hình ảnh thuộc dự án, dữ liệu thư mục và các tài nguyên được khai báo khác.

Hãy coi `build/`, `build/proofs/` và `release/` là ranh giới được sinh. Đừng sửa một lỗi chính tả bằng cách chỉnh một PDF sinh ra, cầu nối `.tex`, bảng kê phát hành hay tệp mã kiểm toàn vẹn.

## Khi một lần tạo lập thành công

Một lần tạo lập thành công nghĩa là tuyến biên dịch đã sản xuất một PDF. Nó **không** có nghĩa cuốn sách đúng về biên tập, đã duyệt về thị giác, tiếp cận được, lưu trữ được, rõ ràng về pháp lý, hay sẵn sàng xuất bản.

Sau mỗi lần sửa quan trọng, hãy soát những trang có thể đã thay đổi: tiêu đề gần điểm ngắt trang, ghi chú, bảng, hình minh họa, chỉ mục, văn bản song song, khảo chú, đầu trang, và các trang cuối của chương là nơi hệ quả bố cục thường xuất hiện.

## Khi một lần kiểm tra báo phát hiện

Sửa các phát hiện `error` trước khi tiếp tục. Điều tra các phát hiện `warning`. Đọc các phát hiện `review` như một yêu cầu tường minh cho phán đoán con người, chứ không phải một thất bại hay phê duyệt tự động.

Tiếp: [Đọc soát bởi con người](human-review.md). Nếu trạng thái sinh có thể lỗi thời, dùng [tạo lập sạch](clean-build.md).
