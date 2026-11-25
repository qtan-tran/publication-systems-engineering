---
title: PSE hoạt động thế nào
description: Hiểu các tầng lõi, hồ sơ, mô-đun ngữ nghĩa và trình bày trong PSE.
---

# Tổng quan kiến trúc

PSE tách ba mối quan tâm: **lõi** dùng chung, các **mô-đun ngữ nghĩa** tái sử dụng, và các **hồ sơ** theo loại ấn phẩm. Cấu hình dự án chọn tính năng được hỗ trợ nào đang hoạt động cho một cuốn sách cụ thể.

Một mô-đun ngữ nghĩa sở hữu nghĩa và dữ liệu ổn định. Một hồ sơ sở hữu trình bày. Chẳng hạn, danh tính người đóng góp là dữ liệu ngữ nghĩa dùng lại được; cách tên người đóng góp xuất hiện dưới tiêu đề một chương trong một sách biên soạn thuộc về hồ sơ edited-collection.

Về hợp đồng chi tiết cho nhà phát triển, xem `/docs/architecture/`.
