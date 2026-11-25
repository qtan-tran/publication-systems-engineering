---
title: Thiết kế chữ và hệ thống trang
description: Hiểu các hợp đồng trình bày lõi cho vai trò thiết kế chữ và hình học trang ổn định.
---

# Thiết kế chữ và hệ thống trang

Thiết kế chữ và hình học trang là **hợp đồng trình bày**, không phải mô-đun ngữ nghĩa. PSE giữ chúng ở tầng lõi/hồ sơ để một tính năng ngữ nghĩa sống sót qua lần thiết kế lại thị giác.

## Vai trò thiết kế chữ

PSE định nghĩa các vai trò có tên cho chính văn, chữ trình diễn, tiêu đề chương, tiêu đề mục và tiểu mục, nhãn và giá trị siêu dữ liệu, đầu trang, chú giải và khảo chú. Các hồ sơ ghi đè giá trị của các vai trò ấy thay vì định nghĩa lại tính năng ngữ nghĩa tiêu thụ chúng.

Chẳng hạn, một ghi chú khảo chú tiêu thụ vai trò thiết kế chữ khảo chú. Mô-đun khảo chú không chọn phông chữ của cuốn sách.

Với thay đổi cục bộ dự án, hãy dùng ranh giới cấu hình cục bộ được hỗ trợ thay vì sửa lõi dùng chung. Xem [Tùy biến thiết kế chữ](../customization/typography.md).

## Hệ thống trang

Hợp đồng hệ thống trang phân giải khoảng trống phía gáy, vùng lề ngoài, vùng trên và dưới, kích thước đầu trang, khoảng cách chân trang, phân bổ khảo chú và độ dài dòng chính văn **trước khi bố cục bắt đầu**. Các mô-đun ngữ nghĩa có thể tiêu thụ những vùng ấy nhưng không được tự động đổi kích thước hệ thống trang sau khi bố cục bắt đầu.

Các chế độ trang hiện hành của hồ sơ đến từ `presentation.json`:

| Hồ sơ | Chế độ trang | Chế độ vật liệu bên |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | `asymmetric-scholarly` | `outer-margin` |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | `asymmetric-scholarly` | `outer-margin` |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | `asymmetric-scholarly` | `outer-margin` |
| [Kịch](../profiles/drama.md) | `asymmetric-scholarly` | `outer-margin` |
| [Tuyển tập](../profiles/edited-collection.md) | `book` | `fallback` |
| [Văn học](../profiles/literary-fiction.md) | `book` | `fallback` |

Chế độ trang của một hồ sơ mô tả đường cơ sở trình bày của nó; nó không ngụ ý mọi đầu sách phải giữ số đo y hệt nhau. Xem [Tùy biến bố cục trang](../customization/page-layout.md).

## Ranh giới thiết kế

Dùng các mô-đun ngữ nghĩa để mô tả ý nghĩa. Dùng các vai trò thiết kế chữ và hệ thống trang để quyết định ý nghĩa ấy trình bày thế nào. Giữ sạch ranh giới này chính là điều cho phép PSE đổi diện mạo một cuốn sách mà không phải viết lại cấu trúc học thuật của nó.
