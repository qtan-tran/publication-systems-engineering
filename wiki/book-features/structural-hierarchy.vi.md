---
title: Phân cấp cấu trúc
description: Dùng hệ phân cấp văn xuôi có giới hạn mà không để hồ sơ trình bày định nghĩa lại độ sâu mục ngữ nghĩa.
---

# Phân cấp cấu trúc

Phân cấp cấu trúc biểu diễn cấu trúc văn xuôi tái sử dụng của một ấn phẩm: phần và chương bao quanh một hệ phân cấp mục có giới hạn. PSE giữ cấu trúc ngữ nghĩa này tách khỏi cách xử lý thị giác của các tiêu đề.

Hợp đồng hiện hành hỗ trợ độ sâu mục tới bốn cấp. `Part` (phần) và `Chapter` (chương) nằm ngoài số đếm này. Cấp mục thứ năm bị từ chối thay vì bị dồn nén im lặng, vì dồn nén im lặng có thể làm thay đổi ý nghĩa và khả năng điều hướng của bản thảo.

## Khi nào dùng

Dùng phân cấp cấu trúc cho những cuốn sách mà lập luận hoặc trình bày được tổ chức qua chương và mục lồng nhau: sách chuyên khảo, tuyển tập, sách văn xuôi nói chung và nhiều ấn bản học thuật. Nó cố tình không được khuyến nghị cho thơ, kịch và văn học khi cấu trúc ngữ nghĩa chính của chúng là thơ, cấu trúc kịch hoặc dòng truyện kể.

## Chính sách hồ sơ

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | bắt buộc | bật |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | khuyến nghị | bật |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | khuyến nghị | bật |
| [Kịch](../profiles/drama.md) | không khuyến nghị | tắt |
| [Tuyển tập](../profiles/edited-collection.md) | bắt buộc | bật |
| [Văn học](../profiles/literary-fiction.md) | không khuyến nghị | tắt |

## Nó sở hữu gì, và không sở hữu gì

Mô-đun `structural-hierarchy` sở hữu **ngữ nghĩa và kiểm định độ sâu mục**. Nó không sở hữu phông chữ, cỡ tiêu đề, khoảng trắng, ngắt trang hay đầu trang. Những thứ đó thuộc hệ thống trình bày lõi/hồ sơ.

Một tùy biến an toàn là đổi cách trình bày tiêu đề nhưng giữ nguyên cấp ngữ nghĩa. Đừng dùng cỡ chữ nhỏ hơn để giả lập một cấp mục bổ sung không được hỗ trợ.

## Quy tắc thực tế

Nếu sự phân biệt phải sống sót qua một lần thiết kế lại hoặc một lần chuyển sang hồ sơ trình bày khác, hãy mô hình hóa nó theo ngữ nghĩa. Nếu đó chỉ là phân biệt thị giác, hãy giữ nó trong cấu hình trình bày.

Xem thêm [Thiết kế chữ và hệ thống trang](typography-and-page-grid.md) và [Chọn hồ sơ trình bày](../getting-started/choose-a-profile.md).
