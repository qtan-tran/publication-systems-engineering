---
title: Bước tiếp theo
description: Đi từ bản tạo lập PSE đầu tiên chạy tốt đến tính năng theo hồ sơ, đọc soát, QA và phát hành.
---

# Bước tiếp theo

Khi một bản khởi đầu tổng hợp đã tạo lập và kiểm tra thành công, hãy thay dần nó bằng nội dung thuộc về dự án. Tiếp tục dùng vòng lặp ngắn sửa/tạo lập/kiểm tra/soát thay vì đợi đến khi toàn bộ bản thảo đã được nhập.

Cho bước học tiếp theo, chọn con đường khớp với công việc của bạn:

- khám phá [Hồ sơ trình bày đầu sách](../profiles/index.md) khi loại ấn bản quyết định bước tiếp theo;
- khám phá [Tính năng sách](../book-features/index.md) cho khảo chú, định vị, văn bản song song hay vật liệu bên lề;
- đọc [PSE hoạt động thế nào](../how-pse-works/architecture-overview.md) khi bạn cần hiểu ranh giới giữa lõi, hồ sơ, mô-đun ngữ nghĩa và nguồn đầu sách;
- dùng [Tùy biến](../customization/typography.md) chỉ sau khi hồ sơ cơ sở đã chạy tốt;
- tiếp tục sang [Chất lượng và phát hành](../quality-release/index.md) trước khi coi một sản phẩm là một ấn phẩm phát hành.

## PDF hoạt động, bản đọc soát và phát hành là ba thứ khác nhau

`pse build` tạo một PDF hoạt động. `pse proof` tạo một sản phẩm đọc soát riêng cho người nhận. `pse release` đưa một bản tạo lập cuối qua hợp đồng phát hành, và `pse verify-release` kiểm chứng bằng chứng phát hành thu được. Đừng dùng một bản tạo lập làm việc bình thường thay cho ranh giới phát hành.

Cẩm nang cho người mới chủ động dừng trước các API hồ sơ nâng cao, việc viết mô-đun ngữ nghĩa, kỹ thuật kiểm toán phát hành và phát triển khung. Đó là những nhiệm vụ riêng, không phải điều kiện tiên quyết để làm cuốn sách đầu tiên của bạn.
