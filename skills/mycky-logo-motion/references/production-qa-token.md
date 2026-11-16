# QA nhiều lớp + tiết kiệm token cho Codex

## 1. Ba cổng độc lập

### Gate A — Geometry (bắt buộc trước animation)
Khóa source glyph, source pose và artwork target đã register. Overlay ink bbox, contours, counters, negative space. Vẽ debug color theo strand, nét giữ C0/C1/tangent; bridge/junction có owner; sections có source thật. Không chấp nhận "font gần giống" khi user có chữ gốc.

### Gate B — Motion (chỉ khi A đạt)
Kiểm thứ tự pha và invariants: chữ nguyên vẹn lúc entry; hold không drift; morph khớp q=0/q=1; không pop ở q=0+; clone spawn trùng; angle monotone và pivot cố định; draw prefix một chiều; star sau đúng gate; shrink một group; wordmark không hiện sớm. Kiểm q tại 0,.05,.1,.25,.5,.75,.9,.95,1 và frame sát tất cả boundary.

### Gate C — Delivery
Render MP4 thật, ffprobe: H.264 high/yuv420p, FPS/duration/size/nb_frames như brief; decode đầu/cuối/đoạn khó/wordmark, xem thật 1× + 0.25×. SHA256/chỉ số kỹ thuật không chứng minh mỹ thuật. Khung cuối phải match artwork và không tự đổi dấu/tên chữ.

## 2. Stop/repair protocol

Khi fail:
1. Lưu **timecode + frame + ROI + expected vs actual**.
2. Chẩn đoán một lỗi: shape mapping? parent transform? ownership? width? timing? codec?
3. Chỉ sửa hàm/phase có owner của lỗi, giữ các pha đúng.
4. Render riêng vùng fail có padding khoảng 0.2–0.4s trước/sau.
5. So trước/sau, nhìn frame và playback thật; nếu đạt mới full render.
6. Sau full render phải kiểm regression toàn bộ phase và file tải/mở.

Không "làm đến hoàn hảo" bằng vòng lặp vô hạn; dùng tiêu chí cụ thể. Khi thiếu ảnh nguồn hoặc chưa xem, ghi PENDING, không báo PASS.

## 3. QA matrix theo loại cảnh

| Cảnh | Chặn lỗi |
|---|---|
| Entry | trọn nét ngoài khung lúc bắt đầu, origin, ink center, scale, no squash |
| Hold | frame-identical về hình, không drift/yoyo |
| Morph | source→target semantic, counter không sập sai, không popping/flicker |
| Crossing | trên/dưới owner rõ, không bệt, không mask phá nét |
| Draw-on | prefix arc-length, hướng đúng, pen-tip sạch |
| Clone/rotate | pivot chung, góc unwrapped, clone ban đầu trùng cha |
| Shrink | group matrix, tỷ lệ/mốc dừng, wordmark không lệch |
| Title | artwork đúng, dấu VN nguyên, font không thay, không hiện sớm |
| MP4 | codec có hỗ trợ rộng, nb_frames đúng, download path verified |

## 4. Các file QA gọn

- qa/observed_timeline.json: PTS/frame có provenance.
- qa/morph_contact.jpg: đủ frame quanh đoạn khó, debug RGBA và final.
- qa/phase_boundary.json: difference q0, q1, hold, failure count.
- qa/final_overlay.png: khác biệt với artwork chính thức đã đăng ký.
- qa/decoded_video.json: metadata từ **video xuất ra**, không chỉ settings.
- qa/qa_report.md: pass/fail/pending có chứng cứ, tránh điền true từ script giả.

## 5. Kiểm soát token và thời gian thực thi

Tránh tiêu tốn như trường hợp chỉ "làm mượt" nhưng mất phần lớn hạn mức:
- Một lần đọc master brief, spec, source files có owner; không nhồi lại toàn repo mỗi lượt.
- Nếu chỉ sửa một morph: render 0.5–1.2s, dùng 8–15 frame debug; không render 8s 10 lần.
- Không tự cài lại GSAP, Remotion, Motion Canvas nếu đã có; không thử concept mới nếu đã chốt.
- Không bắt CODEX viết lại kế hoạch dài khi brief hoàn chỉnh. Prompt ngắn chỉ nói: đọc file → sửa đúng lỗi → check toàn phim → xuất MP4.
- Dùng single source of truth JSON motion spec; bản sửa chỉ patch field changed, không copy hàng ngàn dòng văn.
- Có hai ứng viên kỹ thuật thực sự ngang nhau mới A/B thử cửa sổ ngắn; không sản xuất 5 phương án không có bằng chứng.

## 6. Lệnh bàn giao rút gọn

'Hãy giải nén ZIP, đọc 00_START_HERE.md, 01_MASTER_CODEX_BRIEF.md, 02_MOTION_SPEC.json, tài liệu QA; dùng $mycky-logo-motion. Tiếp tục source hiện tại, khóa concept/thứ tự/artwork, đặc biệt [WINDOW + BUG + EXPECTED]. Tự tìm và sửa nguyên nhân ở anatomy/Bezier/ownership/phase. Render riêng đoạn lỗi, xem từng frame, kiểm lại full MP4 1080×1920/60fps. Chỉ xuất một MP4 cuối sau khi thực sự xem; không cài lại thư viện, không làm lại các đoạn đã đúng.'

## 7. Chẩn đoán một vòng trước khi kết luận

Nếu phát hiện sample tự có rung, nháy hoặc mờ ở phase: mục tiêu là tái dựng **chuyển động có ý nghĩa** sạch hơn sample, không copy lỗi. Nếu source/target quá khác topology, giải thích chính xác đoạn sinh/rút nét cần thiết thay vì nói "morph 100%" không có cơ sở.
