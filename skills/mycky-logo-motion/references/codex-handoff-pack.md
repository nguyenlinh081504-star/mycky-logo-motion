# Gói bàn giao Codex (đúng kiểu người dùng đã chốt)

## 1. Một ZIP triển khai có cấu trúc chuẩn

mycky-project/
- 00_START_HERE.md — một trang: mục tiêu, command, priority, output.
- 01_MASTER_CODEX_BRIEF.md — thứ tự khóa cứng, mô tả chi tiết từng pha, điểm sai nghiêm trọng.
- 02_MOTION_SPEC.json — timeline chuẩn machine-readable, source/target, component ancestry, local/world coordinates, PTS provenance, render constraints.
- 03_QA_AND_ACCEPTANCE.md — các gate PASS/FAIL/PENDING có bằng chứng, ảnh so overlay.
- 04_CODEX_SHORT_COMMAND.txt — một prompt ngắn không bắt Codex lập kế hoạch lại.
- assets/source/ — ảnh glyph gốc, logo đích, nguồn dự án đã được user cấp.
- references/video.mp4 — video mẫu (chỉ chia sẻ riêng trong ZIP của user, **không đẩy lên repo public**).
- source/ — Motion Canvas / pipeline đã hoạt động; không cài lại dependency nếu đã có.
- qa/ — contact sheets, output probe, regression, failure windows.
- final.mp4 — chỉ có khi đã render/QA thực.

## 2. Tài liệu MASTER phải có

Mục tiêu: video reference chỉ khóa choreography, logo đích khóa geometry.

Mỗi phase ghi: start-end, source, immutable properties, owner, target pose, animation mechanism, dependencies, failure checks. Mô tả động tác cụ thể từ endpoint nào, hướng nào, tốc độ nào, nét nào phát triển trong khi nét khác đứng yên. Gắn OBSERVED / PROPOSED.

Một ví dụ:
**JB** — J và B source vào → hold → J chếch lên/B chếch xuống → hold → J/B morph riêng đúng anatomy → rút connectors sau khi morphed → stars → name → final hold. Không chỉ ghi “hai chữ biến hình”.

Một ví dụ:
**CM** — C ngoài thành vòng hở, M trong thành trụ/đỉnh lõm/chân cong **đồng thời**; shared junction; sao chỉ mọc sau khi CM icon sạch.

## 3. Prompt kích hoạt tiết kiệm token

'Giải nén ZIP; đọc 00_START_HERE.md, 01_MASTER_CODEX_BRIEF.md, 02_MOTION_SPEC.json, QA. Dùng $mycky-logo-motion từ repo hiện có; KHÔNG cài lại. Tiếp tục source đang có, giữ nguyên concept/tài nguyên/phần đúng. Ưu tiên sửa đúng cửa sổ [t0,t1]: [lỗi thấy được], expected [đường đi + contour + width + timing]. Tự phát hiện nguyên nhân, sửa mapping/Bezier/pivot/ownership, render đoạn lỗi và kiểm từng frame; sau đó regression toàn video. Chỉ xuất 1 MP4 cuối đúng brief sau khi mở/xem được; không gửi bản thử hay báo cáo dài trừ khi người dùng yêu cầu.'

## 4. Prompt phân tích full timeline

'Đọc video thực (PTS/frame), ảnh nguồn và logo đích. Áp dụng $mycky-logo-motion. Viết TIMELINE TỔNG KẾT đầy đủ từ đầu đến logo cuối: thời gian, phương hướng, hold, từng nét nguồn→đích, điểm neo, junction, width, công thức, lỗi dễ gặp và gate QA. Phân tách observed/proposed. Chỉ dùng video làm tham chiếu nhịp/thứ tự, dựng bản mới sạch hơn lỗi mẫu. Giao đúng timeline, không phát sinh concept.'

## 5. Chính sách nghiệm thu

- Không nói “hoàn hảo/100%” khi chưa nhìn output thật.
- Không dùng video mẫu làm file cuối hoặc dùng frame screenshot để fake vector.
- Không render lại toàn bộ nếu một cửa sổ 0.5 giây còn sai.
- Nếu người dùng chỉ muốn MP4, không ép ZIP/source. Nếu user muốn handoff V12-like, đủ asset/spec/QA.
- Không công khai logos/videos dự án từ thư mục riêng khi chưa có xác nhận quyền phát hành.
