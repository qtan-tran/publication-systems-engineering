---
title: Chuẩn bị phát hành ấn bản
description: Đưa một dự án đã duyệt qua các chốt phát hành của PSE thay vì coi một PDF làm việc là sản phẩm phát hành.
---

# Chuẩn bị phát hành ấn bản

Chỉ tạo một bản phát hành ấn phẩm sau khi đọc soát biên tập và thị giác đã đầy đủ theo chính sách phát hành của bạn.

Từ thư mục gốc dự án:

```text
pse release .
```

Nếu báo cáo máy chỉ còn các phát hiện `review` đã được con người soát và bạn cố ý chấp nhận:

```text
pse release . --acknowledge-review
```

Thao tác phát hành là một lần thăng cấp có chốt, không phải một tên khác của `pse build`.

## Ranh giới phát hành làm gì

PSE tạo lại từ một ranh giới sinh sạch, chạy các chốt QA và soát đầu ra bắt buộc, kiểm chứng bằng chứng ghi nhận nguồn bắt buộc, ghi PDF xuất bản cuối và các tệp bằng chứng vào một thư mục phát hành, và gắn các sản phẩm ấy qua bảng kê phát hành và mã kiểm toàn vẹn.

Thư mục phát hành, chứ không phải `build/book.pdf`, là ranh giới sản phẩm xuất bản.

Các bản phát hành hiện hành dùng schema bảng kê phát hành ấn phẩm `0.2`. Bảng kê gắn PDF cuối với mã SHA-256, số trang/hình học, bằng chứng QA, bằng chứng ghi nhận nguồn bắt buộc, `output-inspection.json`, và `SHA256SUMS.txt` của nó.

## Kỷ nguyên tạo lập tất định tùy chọn

Những người quản lý phát hành cần kiểm soát kỷ nguyên tạo lập tất định có thể dùng:

```text
pse release . --source-date-epoch 1700000000
```

Khi bỏ qua, PSE dùng phương án dự phòng dự án/môi trường được hỗ trợ do phần thực thi phát hành mô tả. Đừng bịa hay làm lệch một kỷ nguyên chỉ để một bản phát hành trông cũ hơn thực tế.

## Kiểm chứng bản phát hành ngay

Sau khi tạo, chạy:

```text
pse verify-release release/<release-id>
```

Việc kiểm chứng kiểm tra hợp đồng phát hành, mã băm sản phẩm, cấu trúc PDF, bằng chứng mã kiểm toàn vẹn và sự gắn kết soát đầu ra schema hiện hành.

Tiếp tục với [Kiểm chứng phát hành](../quality-release/release-verification.md).
