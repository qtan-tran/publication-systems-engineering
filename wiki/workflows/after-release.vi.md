---
title: Sau phát hành
description: Kiểm chứng, bảo quản và kiểm toán các bản phát hành ấn phẩm mà không sửa đổi sản phẩm lịch sử.
---

# Sau phát hành

Hãy coi một bản phát hành ấn phẩm là sản phẩm mang bằng chứng. Đừng chỉnh PDF, bảng kê, báo cáo QA, báo cáo soát hay tệp mã kiểm toàn vẹn của nó tại chỗ để "sửa" lịch sử.

## Kiểm chứng trước khi phân phối hoặc lưu gửi

Chạy:

```text
pse verify-release release/<release-id>
```

Nếu kiểm chứng thất bại, hãy điều tra dự án nguồn và quy trình phát hành. Phát hành lại từ nguồn chuẩn khác với việc sửa thư mục phát hành đã lỗi.

## Bảo toàn ranh giới phát hành

Giữ nguyên thư mục phát hành theo chính sách xuất bản và hồ sơ của bạn. Nếu sau này bạn cần một ấn bản sửa chữa hay bản phát hành sửa chữa mới, hãy tạo một bản phát hành mới từ nguồn với danh tính phát hành và bằng chứng riêng của nó.

## Tạo bằng chứng kiểm toán tách rời khi cần

Với một bản phát hành hiện hành hoặc lịch sử:

```text
pse audit-release /path/to/release --output /path/to/audits/release-audit.json
```

Bản ghi kiểm toán phải nằm ngoài bản phát hành được kiểm toán. Nó ghi lại bằng chứng suy ra từ kiểm chứng mà không sửa đổi bản phát hành.

Với các bộ sưu tập, PSE cũng hỗ trợ `pse audit-index`; các bản ghi/chỉ mục kiểm toán tách rời có thể được kiểm chứng và đóng gói thành một ZIP tất định chỉ chứa bằng chứng. Xem [Bằng chứng kiểm toán](../quality-release/audit-evidence.md).

Với schema bảng kê phát hành cũ `0.1`, đừng chế tạo bằng chứng hiện đại còn thiếu. Xem [Các phát hành trước](../quality-release/historical-releases.md).
