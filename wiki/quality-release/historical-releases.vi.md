---
title: Các phát hành trước
description: Kiểm chứng và đánh giá bằng chứng phát hành lịch sử mà không chế tạo bằng chứng hiện đại hay nâng cấp sản phẩm tại chỗ.
---

# Các phát hành trước

Các bản phát hành PSE hiện hành dùng schema bảng kê phát hành `0.2`. PSE giữ khả năng tương thích chỉ kiểm chứng cho các bản phát hành schema `0.1` hợp lệ về cấu trúc.

Quy tắc chính là: **đừng viết lại bằng chứng lịch sử để nó trông hiện đại.** Một bản phát hành cũ không thể chính đáng có được một báo cáo soát đầu ra vốn không tồn tại vào thời điểm phát hành gốc của nó.

## Kiểm chứng trước

```text
pse verify-release /path/to/historical-release
```

Một bản phát hành `0.1` hợp lệ có thể được kiểm chứng với một cảnh báo tương thích schema. Các phiên bản schema không quen bị từ chối.

## Đánh giá di dời mà không sửa đổi

Dùng:

```text
pse release-migration /path/to/historical-release --human
```

hoặc ghi một bản đánh giá riêng nằm ngoài thư mục phát hành lịch sử:

```text
pse release-migration /path/to/historical-release \
  --output /path/to/audits/release-migration-assessment.json
```

Bản đánh giá không nâng cấp bản phát hành và không suy ra bằng chứng soát lịch sử còn thiếu.

Nếu bằng chứng `0.2` hiện hành đầy đủ là bắt buộc và dự án nguồn gốc vẫn tồn tại, hãy bảo toàn sản phẩm lịch sử và tạo một **bản phát hành mới từ nguồn** bằng môi trường thực thi hiện hành. Điều đó tạo bằng chứng xuất bản mới thay vì thay thế lịch sử.
