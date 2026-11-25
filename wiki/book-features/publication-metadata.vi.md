---
title: Siêu dữ liệu đơn vị xuất bản và người đóng góp
description: Mô tả các đơn vị ấn phẩm tái sử dụng và quan hệ người đóng góp mà không nhân bản danh tính người đóng góp.
---

# Siêu dữ liệu đơn vị xuất bản và người đóng góp

PSE tách biệt **siêu dữ liệu đơn vị ấn phẩm** khỏi **danh tính người đóng góp**. Một đơn vị ấn phẩm có thể là một chương hoặc một đơn vị được mô tả độc lập khác. Một người đóng góp là một người gắn với một hay nhiều đơn vị qua các quan hệ đóng góp.

Một đơn vị ấn phẩm có thể mang ID ổn định, tiêu đề, phụ đề, tóm lược, từ khóa, DOI và các quan hệ đóng góp. Tên, cơ quan và ORCID của người đóng góp thuộc bảng đăng ký người đóng góp và không được sao chép vào từng bản ghi chương.

Điều này quan trọng với sách biên soạn: cùng một người có thể là tác giả của một chương, biên tập viên ở chỗ khác, hoặc giữ vai trò khác trong một đơn vị ấn phẩm khác mà bản ghi danh tính của họ không hề thay đổi.

## Chính sách siêu dữ liệu đơn vị ấn phẩm

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | khuyến nghị | tắt |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | tùy chọn | tắt |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | tùy chọn | tắt |
| [Kịch](../profiles/drama.md) | không khuyến nghị | tắt |
| [Tuyển tập](../profiles/edited-collection.md) | bắt buộc | bật |
| [Văn học](../profiles/literary-fiction.md) | không khuyến nghị | tắt |

## Chính sách siêu dữ liệu người đóng góp

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | khuyến nghị | tắt |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | bắt buộc | bật |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | bắt buộc | bật |
| [Kịch](../profiles/drama.md) | khuyến nghị | tắt |
| [Tuyển tập](../profiles/edited-collection.md) | bắt buộc | bật |
| [Văn học](../profiles/literary-fiction.md) | tùy chọn | tắt |

## Mô hình khuyến nghị

Dùng ID ổn định hướng máy cho đơn vị và người đóng góp. Gắn vai trò vào **quan hệ đóng góp**, không gắn vĩnh viễn vào người. Như vậy tránh được các khẳng định kiểu "người đóng góp này luôn là biên tập viên" khi vai trò phụ thuộc ngữ cảnh.

Với một tuyển tập, cả hai mô-đun đều bắt buộc và hồ sơ trình bày các trang mở đơn vị giàu siêu dữ liệu. Các hồ sơ chuyên khảo và ấn bản có thể kích hoạt siêu dữ liệu đơn vị khi các chương cần siêu dữ liệu độc lập, trong khi siêu dữ liệu người đóng góp vẫn hữu ích ngay cả khi không cần DOI hay tóm lược cho từng chương.

## Ranh giới

PSE không đối chiếu danh tính với các dịch vụ ORCID/ROR bên ngoài, không kiểm định việc đăng ký DOI, và không suy diễn vai trò đóng góp. Những việc đó vẫn thuộc trách nhiệm biên tập hoặc hệ thống bên ngoài.

Xem [hồ sơ Tuyển tập](../profiles/edited-collection.md) để thấy cách dùng mặc định mạnh nhất của mô hình này.
