---
title: Chất lượng và phát hành
description: Hiểu các cấp phát hiện, soát đầu ra, ranh giới sản phẩm, kiểm chứng phát hành và bằng chứng kiểm toán tách rời của PSE.
---

# Chất lượng và phát hành

PSE tách vài loại bằng chứng vì chúng trả lời những câu hỏi khác nhau:

```text
QA máy              → các kiểm tra dự án được khai báo có tìm ra vấn đề cản trở không?
đọc soát con người  → con người đã xét các câu hỏi biên tập và thị giác chưa?
soát đầu ra         → PDF hoàn thành có đạt đường cơ sở kỹ thuật giới hạn không?
hợp đồng phát hành  → PDF và bằng chứng nào cấu thành bản phát hành này?
kiểm chứng phát hành→ bản phát hành ấy còn khớp hợp đồng được ghi của nó không?
bằng chứng kiểm toán→ cái gì có thể được ghi nhận và kiểm tra sau này mà không sửa nó?
```

Không tầng nào trong số này, riêng lẻ hay gộp lại, là khẳng định rằng một cuốn sách không lỗi, rõ ràng về pháp lý, tiếp cận được theo một luật cụ thể, tương thích PDF/UA, lưu trữ được theo một chuẩn cụ thể, hay đúng về trí tuệ.

## Bắt đầu từ đây

- [Mô hình chất lượng](quality-model.md) — `error`, `warning`, `review` và `info`.
- [PDF hoạt động, bản đọc soát và phát hành](artifact-boundaries.md) — ba sản phẩm với ba mục đích khác nhau.
- [Kiểm định đầu ra](output-inspection.md) — đường cơ sở của PDF hoàn thành và giới hạn của nó.
- [Kiểm chứng phát hành](release-verification.md) — kiểm chứng bảng kê, sự gắn PDF, hình học, bằng chứng soát và mã kiểm toàn vẹn.
- [Bằng chứng kiểm toán](audit-evidence.md) — bản ghi kiểm toán phát hành tách rời, chỉ mục, kiểm chứng và xuất bằng chứng tất định.
- [Các phát hành trước](historical-releases.md) — bảo toàn bằng chứng gốc thay vì viết lại lịch sử.
- [Danh sách kiểm tra phát hành](release-checklist.md) — một trình tự xác nhận hoàn tất bởi con người gọn.
