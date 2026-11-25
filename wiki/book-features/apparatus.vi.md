---
title: Khảo chú và các dòng ghi chú
description: Mô hình hóa nghĩa của khảo chú độc lập với nhãn thị giác hay vị trí trình bày mà một hồ sơ ấn bản dùng.
---

# Khảo chú và các dòng ghi chú

Một hệ khảo chú nối vật liệu ghi chú học thuật với một vị trí ổn định trong văn bản. PSE phân biệt **đây là loại ghi chú gì** với **ghi chú ấy được trình bày thế nào**.

Mô-đun khảo chú nhận diện năm dòng ngữ nghĩa:

- `textual` — các phương án đọc và quyết định ấn phê văn bản;
- `editorial` — can thiệp hay giải thích biên tập;
- `translation` — ghi chú hướng dịch thuật;
- `commentary` — bình giảng hay chú giải diễn giải;
- `source` — thông tin về nguồn/bản chứng hoặc hướng nguồn.

Một trình bày có thể hiển thị các dòng ấy với nhãn đầy đủ, chữ viết tắt, hoặc nhãn kiểu A/B/C mà không đổi danh tính ngữ nghĩa của chúng.

## Chính sách hồ sơ

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | tùy chọn | tắt |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | khuyến nghị | tắt |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | bắt buộc | bật |
| [Kịch](../profiles/drama.md) | khuyến nghị | tắt |
| [Tuyển tập](../profiles/edited-collection.md) | tùy chọn | tắt |
| [Văn học](../profiles/literary-fiction.md) | không khuyến nghị | tắt |

Ấn bản khảo cứu yêu cầu và bật hỗ trợ khảo chú. Ấn bản song ngữ và Kịch khuyến nghị nó nhưng để tắt cho đến khi cần. Sách chuyên khảo và Tuyển tập cho phép nó như một năng lực tùy chọn; Văn học không khuyến nghị nó như quy ước khởi đầu.

## Định vị ổn định trước tiên

Một hệ khảo chú chỉ đáng tin ở mức địa chỉ mà nó trỏ tới đáng tin. Hãy ưu tiên định vị ngữ nghĩa hơn số trang PDF để ghi chú vẫn gắn liền khi phân trang thay đổi.

Các lệnh khảo chú chung vẫn được hỗ trợ, nên một dự án không buộc phải phân loại mọi ghi chú sẵn có vào một dòng trước khi tạo lập được.

## Ranh giới

Mô-đun khảo chú sở hữu ngữ nghĩa dòng ghi chú và kiểm định định vị/phạm vi. Thiết kế chữ, nhãn, vị trí chân trang/lề và phân bổ trang thuộc về các hợp đồng trình bày.

Đọc tiếp [Định vị và địa chỉ ổn định](locators.md) hoặc [Lề và nội dung bên](margins-and-side-material.md).
