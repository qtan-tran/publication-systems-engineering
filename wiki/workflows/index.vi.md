---
title: Quy trình sản xuất
description: Dùng một quy trình biên tập hằng ngày ngắn; chỉ khởi chạy đọc soát và kiểm tra phát hành khi cần.
---

# Quy trình sản xuất

PSE hỗ trợ một vòng lặp biên tập thông thường và hai bàn giao sản xuất tùy chọn. Bạn **không** cần thực hiện thủ tục release-engineering sau mỗi lần sửa bản thảo.

| Tình huống | Cần chạy gì | Đọc thêm ở đâu |
| --- | --- | --- |
| Đang biên tập hoặc sửa cuốn sách | `pse build .` → `pse check .` → soát thị giác bởi con người | [Sửa–tạo lập–kiểm tra](edit-build-check.md) |
| Gửi bản đọc cho người nhận | `pse proof . --recipient "Recipient Name"` | [Bản đọc soát cho người nhận](recipient-proofs.md) |
| Xuất bản cuối đã duyệt | `pse release .` → `pse verify-release <release-directory>` | [Phát hành ấn bản](publication-release.md) |

**Khi xử lý sự cố**, dùng [tạo lập lại sạch](clean-build.md). [Đọc soát bởi con người](human-review.md) vẫn cần thiết cho độ chính xác học thuật và chất lượng trang. [Kiểm chứng sau phát hành](after-release.md) và cơ chế bằng chứng phát hành dành cho lưu trữ, kiểm toán và người bảo trì, không phải công việc biên tập hằng ngày.

Hãy sửa bản thảo chuẩn, không phải các tệp trong `build/` hay `release/`. Giữ các thư mục dự án chưa xuất bản ngoài kho nguồn PSE công khai.
