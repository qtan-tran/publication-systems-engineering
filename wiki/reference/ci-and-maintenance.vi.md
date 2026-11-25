# CI và quy trình của người bảo trì

PSE dùng **bốn** workflow GitHub Actions. Vòng lặp chỉnh sửa hằng ngày không phải một nghi lễ phát hành.

| Workflow | Điều kích hoạt | Mục đích |
| --- | --- | --- |
| `qa-regression` | Pull request và main | Kiểm tra nguồn/bảo mật/hợp đồng đã cài; kiểm tra khói PDF nhanh trên PR và kiểm thử thị giác đầy đủ hồ sơ trên main |
| `documentation-pages` | Thay đổi tài liệu hoặc thủ công | Create MkDocs strict, QA site, bằng chứng triển khai Pages |
| `beta-candidate` | Dispatch thủ công | Preflight ứng viên tường minh; không ngụ ý ủy quyền pháp lý |
| `release-evidence` | Dispatch thủ công | Bằng chứng theo commit chính xác trên Windows, macOS và Linux |

**Người biên tập:** `pse build .` → `pse check .` → soát bằng mắt. **Người bảo trì:** chỉ chạy các workflow phát hành đầy đủ cho một commit ứng viên thực sự. Điều này giảm các lần cài lặp lại và các tác vụ TeX dài trong khi giữ sự bảo đảm phát hành khi cần.

Tệp `LICENSE` ở thư mục gốc vẫn vắng mặt trong khi chờ rà soát pháp lý độc lập. Một workflow xanh không bao giờ đủ để tuyên bố trạng thái phát hành có giấy phép công khai, chứng nhận PDF tiếp cận được hay sự sẵn sàng xuất bản chính thức.
