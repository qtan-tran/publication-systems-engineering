---
title: Bản đọc soát cho người nhận
description: Tạo các sản phẩm đọc soát riêng cho từng người nhận mà không lẫn bản đọc soát với PDF làm việc hay bản phát hành ấn phẩm.
---

# Bản đọc soát cho người nhận

Dùng bản đọc soát khi một người hay tổ chức cụ thể cần một bản sao soát được kiểm soát:

```text
pse proof . --recipient "Recipient Name"
```

Có thể ghi một địa chỉ email vào bảng kê đọc soát cục bộ:

```text
pse proof . --recipient "Recipient Name" --email recipient@example.org
```

PSE tạo một PDF có đóng dấu riêng cho từng người nhận dưới `build/proofs/` cùng thông tin lai lịch/mã kiểm toàn vẹn. Mỗi bản đọc nhận một `proof_id`; bạn có thể cung cấp một ID ổn định bằng `--proof-id`, nếu không PSE sẽ sinh nó.

## Một bản đọc soát không phải một bản phát hành

Một bản đọc soát cho người nhận là một sản phẩm phân phối để soát xét. Nó có thể mang các định danh người nhận và bản đọc hiển thị, và có thể vẫn đại diện một ấn phẩm đang thay đổi.

Một bản phát hành ấn phẩm là một trạng thái vòng đời được ủy quyền riêng, tạo bởi `pse release`. Đừng "tạo một bản phát hành" bằng cách xóa dấu bản đọc hay đổi tên một PDF làm việc.

## Ranh giới đóng dấu

Dấu bản đọc hỗ trợ ngăn ngừa và truy nguyên. PSE không tuyên bố đó là DRM không tháo được. Một người xem được PDF có thể rasterize, in/quét, tái tạo hoặc biên tập nó.

Tạo các bản đọc riêng cho từng người nhận bên ngoài khi việc truy nguyên quan trọng. Các bảng kê người nhận có thể chứa dữ liệu cá nhân và thuộc về bộ nhớ riêng tư được kiểm soát, không phải một kho công khai.

Khi sửa đổi được gửi trả, hãy áp chúng vào nguồn chuẩn, tạo lại, kiểm tra, và cấp một bản đọc mới nếu cần thêm một vòng soát.

Tiếp: [Chuẩn bị phát hành ấn bản](publication-release.md).
