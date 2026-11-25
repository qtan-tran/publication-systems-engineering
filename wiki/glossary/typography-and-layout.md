---
title: Thiết kế chữ và chế bản
description: Các khái niệm về typography, bố cục trang, hồ sơ trình bày và nguyên tắc thiết kế theo chức năng của PSE.
---

# Thiết kế chữ và chế bản

Nhóm này tập trung vào cách nội dung được chuyển thành một hình thức có thể đọc được, đồng thời bảo đảm bản sắc thiết kế của từng ấn bản và toàn bộ tủ sách.

| Thuật ngữ | Giải thích |
| --- | --- |
| **Chế bản** (typesetting) | Quá trình chuyển nội dung đã được tổ chức thành những trang sách hoàn chỉnh theo các quy tắc về chữ, lề, khoảng cách, bố cục và phân trang. |
| **Thiết kế chữ** (typography) | Nghệ thuật và hệ thống nguyên tắc sử dụng kiểu chữ, cỡ chữ, độ đậm, khoảng cách và cách sắp xếp chữ để hỗ trợ việc đọc. |
| **Hệ phân cấp thị giác** (visual hierarchy) | Cách sử dụng kích thước, vị trí, độ đậm và khoảng trắng để giúp người đọc nhận ra vai trò và mức độ quan trọng của từng thành phần. |
| **Thang cỡ chữ theo chức năng** (role-based type scale) | Hệ thống cỡ chữ được xác lập theo vai trò nội dung: chính văn, tiêu đề, chú thích, bảng thuật ngữ, niên biểu, thư mục và chỉ mục. |
| **Khoảng cách dòng** (leading) | Khoảng cách theo chiều dọc giữa các dòng chữ, thường được đo giữa hai đường chân chữ liên tiếp. |
| **Khổ sách** (trim size) | Kích thước vật lý cuối cùng của một trang sách sau khi cắt xén. |
| **Khối chữ** (text block) | Vùng chính trên trang dành cho nội dung văn bản. |
| **Lề trong** (inner margin) | Khoảng trắng ở phía gần gáy sách. |
| **Lề ngoài** (outer margin) | Khoảng trắng ở phía đối diện gáy sách, có thể chứa dấu chỉ vị trí hoặc ghi chú bên lề. |
| **Trang phải và trang trái** (recto/verso) | Hai loại trang trong sách mở đối diện. Chúng thường có bố cục lề đối xứng qua gáy. |
| **Đầu trang** (header) | Vùng phía trên khối chữ, có thể chứa tên tác phẩm, tên chương hoặc thông tin định hướng. |
| **Chân trang** (footer) | Vùng phía dưới khối chữ, thường dành cho số trang hoặc thông tin phụ. |
| **Tiêu đề nhóm chỉ mục** (index heading) | Tiêu đề phân chia các nhóm mục từ, thường là các chữ cái A, B, C hoặc một nhóm chủ đề. |
| **Kiểu trang** (page style) | Tập hợp quy tắc quy định cách trình bày đầu trang, chân trang, số trang và các yếu tố lặp lại. |
| **Nhúng phông chữ** (font embedding) | Đưa dữ liệu phông chữ cần thiết vào tệp PDF để người đọc có thể xem tài liệu đúng hình thức mà không cần cài sẵn phông tương ứng. |
| **Hình ảnh vectơ** (vector graphics) | Hình ảnh được mô tả bằng đường nét và hình học, có thể phóng lớn mà không bị vỡ hạt như ảnh điểm ảnh. |
| **Trang thông tin chế bản** (colophon) | Phần ghi nhận thông tin về quá trình sản xuất sách, chẳng hạn công cụ chế bản, phông chữ, thiết kế, phiên bản và đơn vị thực hiện. |

## Thiết kế theo chức năng thay vì định dạng thủ công

Nếu mỗi tiêu đề được chỉnh riêng bằng định dạng trực tiếp, các thành phần cùng vai trò dễ phát sinh khác biệt ngoài chủ ý. Ngược lại, khi thiết kế theo chức năng, các thành phần cùng chức năng dùng chung một quy tắc: mọi tiêu đề chương, mọi chú thích, mọi bảng biểu đều nhận hình thức từ định nghĩa vai trò của chúng.

Thang cỡ chữ theo chức năng không có nghĩa mọi phần trong cuốn sách đều dùng một cỡ chữ, cũng không có nghĩa mọi cuốn trong tủ sách đều phải giống hệt nhau. Trong *Nữ Bái Thần*, chính văn, niên biểu và thư mục từng được điều chỉnh theo nhu cầu đọc và mật độ thông tin riêng. Đây là ví dụ cho thấy một hệ thống thiết kế cần vừa có quy tắc chung, vừa cho phép ngoại lệ có chủ ý và được ghi nhận.

## Các khái niệm về kiến trúc thiết kế PSE

| Thuật ngữ | Giải thích |
| --- | --- |
| **Mẫu chế bản** (template) | Một cấu hình hoặc bộ quy tắc có thể tái sử dụng để tạo ra sách với hình thức nhất quán. |
| **Hồ sơ trình bày** (presentation profile) | Tập hợp quy tắc phù hợp với một loại hình ấn bản, chẳng hạn kịch, giáo trình hoặc sách chuyên khảo. |
| **Mô-đun nội dung** (semantic module) | Thành phần chức năng có thể tái sử dụng, chẳng hạn bảng thuật ngữ, niên biểu, khảo chú hoặc chỉ mục. |
| **Hệ thống lõi dùng chung** (shared core) | Phần quy tắc, công cụ và chức năng nền tảng được nhiều dự án sách sử dụng. |
| **Điều chỉnh riêng đầu sách** (title-local override) | Một thay đổi chỉ áp dụng cho một đầu sách, nhằm đáp ứng đặc điểm riêng mà không làm thay đổi quy tắc chung của các sách khác. |
| **Ngoại lệ thiết kế** (design exception) | Quyết định có chủ ý không tuân theo một quy tắc mặc định vì có căn cứ nội dung, thẩm mỹ hoặc chức năng cụ thể. |

**Tính nhất quán không đồng nghĩa với tính đồng nhất.** Một hệ thống xuất bản có khả năng mở rộng phải cho phép những đầu sách khác nhau duy trì đặc điểm riêng trong một kiến trúc thiết kế chung.

Bảng thuật ngữ liên quan: [Tạo lập ấn bản và phiên bản](build-and-versioning.md), tổng quan về hồ sơ trình bày ở phần [Book Profiles](../profiles/index.md).
