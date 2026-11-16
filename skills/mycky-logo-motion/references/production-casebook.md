# Production casebook — 12 bài thực chiến / công thức chọn theo geometry

**Nguồn:** Bản tóm tắt từ các lượt phân tích video/brief thực tế của người dùng. Những mốc sau là ghi chép từ quá trình phân tích trước, **không phải keyframe gốc**. Khi có clip trong project mới, đo lại bằng ffprobe/PTS và đối chiếu frame. Không đặt video/logo của khách vào repository công khai. Các ca chỉ minh họa **cơ chế**; không tái sử dụng hình dạng hoặc tọa độ.

## 1. CIMUNA — C/M thường → vòng C và hai trụ M cong

- **Pha:** C từ trái + M từ phải → đứng nguyên glyph đến ~1.33s → cùng morph 1.33–1.97s → giữ icon chưa có sao → sao bốn cánh ở đỉnh → sao hạ xuống kéo nét nối dọc → group shrink → CIMUNA wordmark → hold.
- **Khóa asset:** đúng C và M dạng béo người dùng cấp; không font gần giống, không biến trong entry/hold. Tên đích CIMUNA, trong khi clip có thể hiện tên khác.
- **Ancestry C:** cung trên, sống trái dày, cung đáy, đầu mở trên phải và đầu mở dưới phải. Hai đầu phải luôn hở, không đổi sang O.
- **Ancestry M:** hai trụ, hai nhánh xiên tạo V và nút V. Nút V nâng lên thành lõm đỉnh; trụ kéo dài thành hai thân/chan cong nối đáy C. Junction chân M phải lấy tọa độ C tại frame hiện tại, không tween rời.
- **Microphase đề xuất:** 1.333–1.467 nhận diện chữ; 1.467–1.600 lồng và thu V; 1.600–1.733 tạo vòng/thân cong; 1.733–1.867 dày–mỏng và giao; 1.867–1.967 khóa pose. ~1.73–1.87 dễ bị pop, chồng đen.
- **Chọn F16/F17/F19; F34, F35, F36**. QA: tách màu C/M, bốn điểm nối, điểm lõm M, q=0/1 coverage; sao không xuất hiện trước khi CM hoàn thành.

## 2. SON MUSIC — S thường → S thư pháp nhiều nhánh + đường chéo

- **Pha nguồn ~4.17s:** S béo hold → nét đầu S mới từ trên phải vòng sang trái → S cũ chuyển xám/mất trong khi nét mới phát triển (đúng clip có layer fade) → thân S, vòng chân ngoài, móc trong → hold ~0.57s → vòng trang trí trên phải → đường chéo đi từ trên xuống → đầu nhọn hình thoi → hold.
- **Khoảng tham chiếu:** 0.30–1.90 vẽ S cách điệu; ~1.93–2.50 hold; 2.53–3.67 vòng trên/đường chéo/hình thoi. Clip không có SON MUSIC; phần thu và wordmark là đề xuất.
- **Tách 7 owner:** S0 glyph cũ; S1 thân chính; S2 nét song song/vòng chân; S3 móc trong; S4 vòng trang trí trên; S5 đường chéo; S6 đầu nhọn.
- **Điểm QA:** vòng dưới được vẽ trước móc trong, nét chéo chỉ vẽ sau nhịp dừng, hình thoi mọc ở đầu đường chéo, không pop. Đường cong dùng prefix arc-length, width profile. S0 opacity là ngoại lệ **do clip có**, không phải giấy phép fade mọi morph.
- **F27/F28/F29 + F35/F36.** Lock wordmark SON MUSIC nguyên artwork.

## 3. ELAW VIỆT — E + búa tham chiếu → E lõi + 3 nét → xoay

- **Pha:** E đen đi từ trái, búa thẩm phán từ phải → hold → búa mờ/exit, E tiến tâm và chuyển sang E vuông lõi → hold → ba nét ngang phát triển đồng thời về trái → hold → cả nhóm xoay ngược chiều kim đồng hồ → thêm shrink/ELAW VIỆT theo artwork nếu clip chỉ có xoay.
- **Cơ chế ba nét:** thanh ngoài trên, thanh ngoài dưới và đường kéo dài từ giữa E; 3 thanh bắt đầu gần như đồng thời. Mốc phân tích trước: ~1.97–2.57s, tiến độ xấp xỉ 0/37/72/92/100% ở t≈1.97/2.20/2.30/2.40/2.57. Đây là tỷ lệ quan sát xấp xỉ, phải đo lại nếu dùng.
- **Cơ chế xoay:** riêng icon đầy đủ xoay, không cho ba thanh xoay riêng. Clip khảo sát tới ~−32.6° ở 2.97s; artwork khoảng −40.3° là đích bổ sung. Pivot mẫu được ước lượng gần (368.5,523) trên 720×1280, không dùng như tọa độ canvas 1080×1920.
- **QA:** chữ E gốc giữ form trước morph; ba đầu bút sạch và đồng nhịp; một parent rotation; dấu VIỆT lấy từ artwork. Không gán búa thành nét source của E (búa là footage tham chiếu).

## 4. SQUIVA — S thường + ảnh sóc → S đuôi sóc rồi thêm sóc

- **Pha video ~6.77s:** S từ trái + ảnh sóc từ phải → hold → hai nét đỏ tô đường S/đuôi sóc để giải thích → loại ảnh tham chiếu và đường đỏ → S trung tâm → S béo morph thành S đuôi tròn lớn → hold → silhouette đầu/tai/thân/chân sóc hiện phía trái → hold icon. Wordmark SQUIVA là pha **PROPOSED** vì clip không có.
- **Morph S ~4.07–4.73:** S_TOP mở to thành phần đuôi tròn; S_WAIST giữ nối cong; S_BOTTOM nở chân; S_NEGATIVE khóa dải trắng bên trong. Không morph ảnh sóc vào chữ S bằng đè ảnh.
- **Sóc ~5.63–5.90:** head, ears, nose, foreleg, haunch và trắng phân cách có path riêng; silhouette sóc có thể reveal/opacity nếu đúng video mẫu, nhưng geometry phải khớp đích, không ghép bộ phận rời.
- **QA:** giữ S cách điệu hoàn thành **trước** khi sóc hiện; vùng trắng không bị đóng; chữ Q của SQUIVA giữ nguyên đuôi từ artwork.

## 5. GRIT BODY — GB đỏ → GB vuông + thanh nối mọc giữa

- **Pha video ~8s:** tạ lên và hold → G đỏ trái/B đỏ phải vào rồi hold → G/B biến thành nét góc cạnh trong khi tạ mờ → GB đen riêng biệt hold → thanh nối sinh ở tâm khe rồi mở đồng thời sang trái/phải → icon GB hoàn thành. Chữ GRIT BODY bổ sung sau clip.
- **G:** cung ngoài tròn thành cạnh đứng + vát; đầu trên vẫn mở; thanh ngang giữa không tách. **B:** trụ trái vẫn thẳng, hai bowl tròn thành hình thang/góc, hai counters còn nguyên, eo tạo góc rõ.
- **Nét nối ~6.93–7.8:** start ~center x=358 (video 720×960), xL=c−Lleft·q và xR=c+Lright·q. Không vẽ từ trái sang phải. Junction phải gắn vào G/B tại cùng thời điểm; không ăn vào counter B.
- **QA:** giữ counters B, gap G, tạ chỉ opacity phụ; sau morph hold rồi mới nối; các góc vát đúng ảnh đích.

## 6. ASH XANH — AX + lửa/củi → A + X góc mở

- **Video mẫu ~4.67s, 133 decoded frames:** có frame giãn ở đầu, cần PTS thật, không lấy k/30. A phía trên/X phía dưới từ trái vào; lửa và củi từ phải vào → hold → lửa tách lên khỏi củi → A vào lửa, X vào củi → footage mờ đi → A/X thành hình học đen → tách mảnh chân phải A cuối → giữ icon. Wordmark ASH XANH thêm sau clip.
- **A:** left/right legs bảo toàn vai, bar chuyển thành hệ góc bên trong, counter thành khe nghiêng, chân phải sau morph mới được tách bởi khe chéo cục bộ; không dùng rectangle trắng xóa contour.
- **X:** hai thanh thay đổi tương đối từ ±59° gần thẳng đứng sang ±15° gần nằm ngang. Phải xoay và đổi chiều dài **từng nhánh quanh nút chung**, không quay cả X như một khối (góc giữa hai nhánh không đổi khi rigid rotate).
- **QA:** lửa/củi là layer ảnh phụ mờ đi, không chính là glyph ancestry; tách phần chân phải A chỉ sau khi AX góc cạnh hoàn thành; hai thanh X giữ thẳng, giao ở tâm; không mất mảnh A.

## 7. BLING BLING — B béo → B swash có đuôi

- B gốc giữ hai counters, thân, bowl trên/bowl dưới; morph từ chữ thường sang ribbon cần phối chiều dài đường hiện thực với width. Bản từng bị "nháy một phát": việc geometry dồn vào giữa clip không thể sửa bằng blur.
- Cần q→visible geometry metric arc-length time reparameterization; kiểm counter mapping theo anatomy và đầu/đuôi; kiểm 0,0+ coverage. Font chữ thương hiệu phải lấy artwork.
- F02/F31, width/tangent và local QA. Tạo overlay tại tất cả frame morph, không nhìn chỉ frame đầu/cuối.

## 8. JIA BEAUTY / JB — hai chữ reposition → morph riêng → rút cầu sau

- J và B thường từ hai phía vào rồi hold, **cỡ đầu vừa phải** và căn thẳng. J dịch chếch lên, B chếch xuống để vào nơi của mỗi phần icon → hold → **morph riêng** J và B vào hình stylized; xong mới được rút connecting strokes; sao rồi tên.
- Đáy B và counter B rất dễ lỗi; cleanup chỉ vùng cầu tạm có ownership, không xóa mất phần dưới B. Không được trông như từng mảnh icon bay vào lắp.
- F19/F16/F17/F32. Gate: original ink-bbox center, scale, anatomical correspondence J/B, 2 counters B (nếu target có), final icon trước accent.

## 9. FANTASHION — F béo trước xoay, sau mới vẽ ornament

- Chữ F gốc từ trái vào → dừng nguyên nét → clone theo parent và xoay lần lượt từng +90° quanh một pivot chung → hold cả cụm F béo → **sau đó** mới phát triển ornamental strokes → shrink → wordmark.
- Bài học: font "F gầy" khi quay là sai; không thay image SDF/shape trước khi phép quay hoàn tất. Ghi đặc tả góc, tránh wrap −270/90 gây đảo. Nếu xoay chồng làm mảng đen quá dày, chọn choreography sạch nhưng vẫn bám mẫu, giải thích khác biệt.
- F25/F26 và precision-refinements A; kiểm clone birth trùng pose cha, 90/180/270, min radius, width bất biến qua pha rotate.

## 10. LUMI — L gốc biến rồi clone đúng một nét

- L từ **phải** vào, dừng đúng tâm ink bbox (nếu brief yêu cầu nhích cao, dùng offset world có chủ đích) → L thường morph thành L cách điệu → giữ L đó làm source → nhân bản nét y hệt → **chỉ bản sao xoay** để lắp icon → sao trung tâm **sau khi icon khớp** → chữ Lumi.
- Không tự font hoặc rectangle thay L nguồn; nguyên bản L đứng yên khi clone xoay; stage order là điều kiện bắt buộc.

## 11. OHANA Talents — H giữ bridge + O vòng

- O/H xuất hiện theo thứ tự, H gồm thân trái, thân phải, bridge; thân trái uốn thành vòng móc dưới, thân phải phát triển cung trên; bridge bắt buộc giữ gắn hai thân suốt morph. O có outer/inner contour riêng.
- Sao/tên chỉ sau icon hoàn thiện; không dựng nhánh H rời khiến hình bị cắt giữa. F11/F16/F17; kiểm bridge endpoint từ hai thân hiện tại thay vì tween độc lập.

## 12. HOA ĐỎ / HD — H thân cây + vòng hoa

- H và Đ từ ngoài vào → giữ, dịch xuống/scale lớn nhẹ nếu brief → Đ mờ rút khỏi cảnh → H tiến tâm, rút thanh giữa thành trụ cây → nét vòng xuất phát từ trên phải H, chạy xuống phải, qua đáy sang trái rồi hướng lên theo path đã khóa → hoa xuất hiện theo chỉ dẫn (có thể instantly, không mặc định nở dần) → shrink vào bố cục → tên Hoa Đỏ.
- Phân biệt Đ exit bằng opacity với biến hình H bằng geometry; hoa thời điểm riêng, không xuất hiện trước vòng. F27/F28/F35/F36.

## 13. JK / Butterfly S — bài học phụ thuộc

- **JK:** J/K nguồn vào từ ngoài → hold → J và K đến vị trí icon → hold → mỗi chữ morph thành stylized riêng → rút connectors **sau** morph → crown từ trên → name. Không cho icon mọc thành một cục.
- **Butterfly S:** hai chữ S từ hai phía vào → cùng biến thành hai đường S-cong riêng → phối thành butterfly rồi mới có thân/cánh/wordmark đúng artwork. Không tự cho hai S mất rồi bật butterfly hoàn chỉnh.

## 14. Quy tắc chung rút ra

1. Không thể dùng một animation formula cho mọi logo. Chọn theo shape ancestry, counters, repeated modules, crossing.
2. Không dùng tên chữ để suy đoán motif; artwork và video mẫu quyết định.
3. Luôn nói rõ **sample đã có** và **phần bổ sung để khớp logo khách**.
4. Để làm mượt: sửa geometry correspondence trước, timing/velocity sau.
5. Khi user chỉ yêu cầu sửa một đoạn, không rebuild toàn video; nhưng full-regression QA trước giao.
6. Không hứa khớp 100% nếu thiếu asset, không có clip thực hoặc chưa xem full render.
