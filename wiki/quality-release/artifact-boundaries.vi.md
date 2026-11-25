---
title: PDF hoạt động, bản đọc soát và phát hành
description: Phân biệt sản phẩm lặp lại, sản phẩm đọc soát riêng cho từng người nhận, và bản phát hành ấn phẩm mang bằng chứng.
---

# PDF hoạt động, bản đọc soát và phát hành

Những PDF này có thể trông giống nhau trên màn hình, nhưng chúng mang nghĩa vòng đời khác nhau.

| Sản phẩm | Được tạo bởi | Vị trí điển hình | Mục đích |
| --- | --- | --- | --- |
| PDF hoạt động | `pse build .` | `build/book.pdf` | lặp lại và soát cục bộ |
| Bản đọc soát cho người nhận | `pse proof . --recipient ...` | `build/proofs/` | soát xét bên ngoài/nội bộ được kiểm soát với danh tính người nhận |
| Bản phát hành ấn phẩm | `pse release .` | `release/<release-id>/` | ranh giới sản phẩm xuất bản cuối mang bằng chứng |

## PDF hoạt động

Một PDF hoạt động là sản phẩm tạo lập dùng xong bỏ. Hãy tạo lại nó khi dự án thay đổi. Đừng lưu gửi hay lưu trữ nó như thể nó là hợp đồng phát hành.

## Bản đọc soát cho người nhận

Một bản đọc soát gắn với tên người nhận/danh tính bản đọc và được đóng dấu để ngăn ngừa và truy nguyên. Nó không phải một bản phát hành sạch và có thể vẫn chứa nội dung đang chờ sửa.

## Bản phát hành ấn phẩm

Một bản phát hành được tạo độc lập qua các chốt phát hành. PDF của nó được gắn với bằng chứng đọc được bằng máy và mã kiểm toàn vẹn. Một bản phát hành **không** phải "bản đọc không có dấu", và một bản đọc **không** phải "bản phát hành cộng thêm một dấu".

Sự phân biệt này ngăn phân phối nhầm sản phẩm vòng đời sai và làm cho việc kiểm chứng về sau có nghĩa.
