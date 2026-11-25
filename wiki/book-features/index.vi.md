---
title: Tính năng sách
description: Dùng các năng lực tái sử dụng của PSE mà không lẫn cấu trúc ngữ nghĩa với trình bày của hồ sơ.
---

# Tính năng sách

PSE tách biệt **tính năng sách** khỏi **hồ sơ sách**. Một hồ sơ trả lời "ta đang sản xuất loại ấn phẩm nào?". Một tính năng trả lời "ấn phẩm này cần năng lực ngữ nghĩa hay trình bày nào có thể tái sử dụng?".

Sự phân biệt này quan trọng vì cùng một năng lực có thể xuất hiện ở nhiều loại ấn bản. Một chỉ mục có thể thuộc một sách chuyên khảo, một ấn bản khảo cứu hay một vở kịch. Siêu dữ liệu người đóng góp có thể mô tả một tuyển tập, một ấn bản song ngữ hay một ấn bản học thuật. Một vật thể lề có thể được đặt cạnh chính văn ở hồ sơ này và rơi về dòng chảy đọc trong hồ sơ khác.

## Cẩm nang tính năng

- [Phân cấp cấu trúc](structural-hierarchy.md) — phần, chương, mục và ranh giới độ sâu được hỗ trợ.
- [Siêu dữ liệu đơn vị xuất bản và người đóng góp](publication-metadata.md) — các đơn vị kiểu chương, tóm lược, từ khóa, DOI, người đóng góp, cơ quan và vai trò.
- [Thiết kế chữ và hệ thống trang](typography-and-page-grid.md) — các vai trò trình bày, hình học trang, và ranh giới giữa mô-đun ngữ nghĩa và bố cục.
- [Lề và nội dung bên](margins-and-side-material.md) — ghi chú lề, chú giải bên, điểm neo, dấu chỉ và fallback tất định.
- [Văn bản song song](parallel-text.md) — các đoạn nguồn/đích ổn định, đối ứng, ghi chú, định vị và các chế độ bố cục.
- [Khảo chú](apparatus.md) — các dòng textual, editorial, translation, commentary và source.
- [Định vị và địa chỉ ổn định](locators.md) — các hệ địa chỉ canonical, dramatic-line, verse-line và parallel-alignment.
- [Ngữ nghĩa thơ và kịch](verse-and-drama.md) — khổ thơ, dòng thơ, nhân vật thoại, lời thoại, chỉ dẫn sân khấu, màn và cảnh.
- [Thư mục, chỉ dẫn và vật liệu học thuật](bibliography-index-scholarly-matter.md) — trang đầu/cuốn học thuật dùng lại được và các cấu trúc truy xuất.
- [Văn bản đa ngôn ngữ](multilingual-text.md) — văn bản nhận thức ngôn ngữ, tiếng Hy Lạp đa dấu và hỗ trợ chuyển tự.

## Đọc các bảng chính sách thế nào

Các trang tính năng chỉ sao chép chính sách hồ sơ ở nơi bảng kê hồ sơ khai báo tường minh. Các trạng thái có nghĩa:

- `required` (bắt buộc) — hồ sơ phụ thuộc vào năng lực này;
- `recommended` (khuyến nghị) — thường phù hợp về biên tập, nhưng không bắt buộc về cấu trúc;
- `optional` (tùy chọn) — được hỗ trợ khi dự án cần;
- `discouraged` (không khuyến nghị) — về mặt kỹ thuật khả thi nhưng thường là mặc định kém cho loại ấn phẩm ấy;
- `incompatible` (không tương thích) — dành cho xung đột cùng tồn tại thực sự về ngữ nghĩa hoặc kỹ thuật.

`not declared` (không khai báo) **không** có nghĩa không tương thích. Nó nghĩa là hồ sơ khởi đầu hiện hành không có mục chính sách tường minh cho mô-đun ấy. Các bảng trong cẩm nang này được kiểm thử hồi quy đối chiếu với các bảng kê `profile.json` công khai, nên phần diễn giải không thể lặng lẽ trở thành một nguồn sự thật thứ hai.

Các năng lực trình bày seperti vai trò thiết kế chữ và hệ thống trang là hợp đồng lõi/hồ sơ chứ không phải mô-đun ngữ nghĩa, nên chúng dùng chỉ mô tả trình bày thay vì trạng thái chính sách mô-đun.
