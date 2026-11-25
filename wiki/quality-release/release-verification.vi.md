---
title: Kiểm chứng phát hành
description: Kiểm chứng rằng một bản phát hành sẵn có vẫn khớp bảng kê, hợp đồng PDF, bằng chứng soát đầu ra và mã kiểm toàn vẹn của nó.
---

# Kiểm chứng phát hành

Chạy:

```text
pse verify-release /path/to/release
```

Với một bản phát hành schema bảng kê hiện hành `0.2`, việc kiểm chứng kiểm tra hợp đồng bảng kê phát hành công khai, mã kiểm toàn vẹn PDF cuối, số trang và hình học, hợp đồng soát đầu ra và sự gắn mã băm PDF, cùng bằng chứng `SHA256SUMS.txt`.

Một lần đạt nghĩa là các sản phẩm được kiểm tra thỏa các hợp đồng được ghi dưới bộ kiểm chứng đã cài. Nó không kiểm định độc lập độ đúng biên tập, mức rõ ràng quyền, chứng nhận tiếp cận hay trạng thái kho lưu trữ.

## Khám phá hợp đồng

Người kiểm toán và công cụ có thể khảo sát bề mặt schema công khai đã cài bằng:

```text
pse contracts
pse contracts --json
```

Lệnh này phân giải môi trường thực thi đang hoạt động thay vì giả định một bản checkout nguồn.

## Nếu kiểm chứng thất bại

Đừng làm bảng kê "khớp" bằng cách làm mới mã băm bằng tay hay chỉnh các tệp bằng chứng. Hãy điều tra xem bản phát hành chưa hoàn chỉnh, hư hỏng, bị thay đổi hay không được hỗ trợ. Nếu một ấn phẩm phải được sửa, hãy quay về nguồn chuẩn và tạo một bản phát hành mới qua tuyến phát hành bình thường.

Với hỗ trợ chỉ kiểm chứng của schema `0.1`, xem [Các phát hành trước](historical-releases.md).
