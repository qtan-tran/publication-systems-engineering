---
title: Lề và nội dung bên
description: Biểu diễn vật liệu bên bằng ngữ nghĩa và bảo toàn nó qua fallback tất định khi không đặt được vào lề.
---

# Lề và nội dung bên

PSE có thể biểu diễn vật liệu có thể xuất hiện bên cạnh chính văn, mà không làm "nằm trong lề" thành một phần danh tính ngữ nghĩa của vật thể.

Mô-đun `margin-objects` cung cấp ID ổn định cho năm loại vật thể: ghi chú lề, chú giải bên, điểm neo khảo chú, dấu chỉ định vị, và vật thể chạy bên. Một hồ sơ hoặc dự án quyết định những vật thể ấy xuất hiện ở lề ngoài hay dùng trình bày fallback hiển thị trong dòng chảy đọc chính.

Fallback ấy quan trọng: PSE không im lặng loại bỏ nội dung ngữ nghĩa chỉ vì một thiết kế trang thiếu chỗ bên.

## Chính sách hồ sơ

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | khuyến nghị | tắt |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | khuyến nghị | tắt |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | khuyến nghị | bật |
| [Kịch](../profiles/drama.md) | khuyến nghị | tắt |
| [Tuyển tập](../profiles/edited-collection.md) | tùy chọn | tắt |
| [Văn học](../profiles/literary-fiction.md) | tùy chọn | tắt |

Các ấn bản khảo cứu bật vật thể lề theo mặc định. Vài hồ sơ khác khuyến nghị hoặc cho phép chúng nhưng để tắt trong bản khởi đầu, để bản thảo không tự thu thêm vật liệu bên mà thực tế không cần.

## Khi nào dùng vật thể lề

Dùng khi nội dung có danh tính biên tập ổn định cần sống sót qua thay đổi trình bày. Đừng dùng chỉ để đẩy văn xuôi thường ra bên vì hiệu ứng thị giác.

Các trường hợp điển hình gồm một chú giải lề ngắn, một chú giải bên gắn với vật thể kiểu hình, một dấu chỉ định vị, hoặc một điểm neo khảo chú ngữ nghĩa.

## Ranh giới trình bày và tiếp cận

Đặt vào lề ngoài là một lựa chọn thị giác. Nó tự thân không thiết lập thứ tự đọc tagged-PDF hay sự tuân thủ tiếp cận. Khi không đặt được vào lề, hợp đồng mặc định giữ vật thể hiển thị trong dòng chảy đọc chính, thay vì giả vờ nội dung ấy là tùy chọn.

Về hình học trang, xem [Thiết kế chữ và hệ thống trang](typography-and-page-grid.md).
