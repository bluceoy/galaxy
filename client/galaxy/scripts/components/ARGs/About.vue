<template>
    <div>
        <div class="wrap">
            <div class="note">
                <p>This website is managed by The Environmental Biotechnology Laboratory of The University of Hong Kong.</p>
                <p>Should you have any queries or require further information, please do no hesitate to contact us here.</p>
            </div>
            <h1>Team</h1>
            <div class="flex-wrap">
                <div class="item">
                    <div class="avatar">
                        <img src="/static/args/about/Tong.00b67e94.jpg" alt="" width="100%">
                    </div>
                    <div class="info">
                        <h4>Ir. Dr. Tong ZHANG</h4>
                        <p class="desc">Professor</p>
                        <p class="desc">Environmental Biotechnology Lab</p>
                        <p class="desc">University of Hong Kong</p>
                        <h5>Research interests:</h5>
                        <ul>
                            <li>Microbial population dynamics in full-scale WWTPs</li>
                            <li>Major functional groups in biological wastewater treatment</li>
                            <li>Antibiotics and antibiotics resistance genes in WWTPs and related environments</li>
                            <li>Novel microbial populations and genes in waste/wastewater treatment</li>
                        </ul>
                    </div>
                    <div class="link">
                        <a class="btn"></a>
                        <a class="btn"></a>
                        <a class="btn"></a>
                    </div>
                </div>
                <div class="item">
                    <div class="avatar">
                        <img src="/static/args/about/Anni.9584d16a.jpg" alt="" width="100%">
                    </div>
                    <div class="info">
                        <h4>Ir. Dr. Tong ZHANG</h4>
                        <p class="desc">Post-doc</p>
                        <p class="desc">Alm Lab</p>
                        <p class="desc">Biological Engineering</p>
                        <p class="desc">MIT</p>
                        <h5>Research interests:</h5>
                        <ul>
                            <li>Bioinformatics pipeline development and big data analysis</li>
                            <li>Information integration and visualization</li>
                            <li>Antibiotic resistance and mobile genetic elements</li>
                            <li>Microbial metabolism</li>
                        </ul>
                    </div>
                    <div class="link">
                        <a class="btn"></a>
                        <a class="btn"></a>
                        <a class="btn"></a>
                        <a class="btn"></a>
                        <a class="btn"></a>
                    </div>
                </div>
                <div class="item">
                    <div class="avatar">
                        <img src="/static/args/about/Bryan.d43ea8d1.jpg" alt="" width="100%">
                    </div>
                    <div class="info">
                        <h4>Chen-Ju Bryan HOU</h4>
                        <p class="desc">Research Assistant</p>
                        <p class="desc">Environmental Biotechnology Lab</p>
                        <p class="desc">University of Hong Kong</p>
                    </div>
                    <div class="link">
                        <a class="btn"></a>
                        <a class="btn"></a>
                        <a class="btn"></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
* {
    padding: 0;
    margin: 0;
}
.wrap {
  margin: 0 auto;
  width: 90%;
}
.note {
  border-left: 5px solid #ccc;
  padding: 5px 15px;
  margin: 35px 0;
}
.note p {
  padding: 3px;
}
h1 {
  padding: 5px 0;
}
.flex-wrap {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 50px;
}
.flex-wrap .item {
  width: 300px;
  height: 650px;
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  margin-right: 15px;
}
.flex-wrap .item .info {
  padding: 10px;
}
.flex-wrap .item .info .desc {
  font-size: 14px;
  padding: 1px 0;
  color: rgba(0,0,0,.4);
}
.flex-wrap .item .info ul {
  padding: 10px 10px 10px 40px;
}
.flex-wrap .item .info ul li {
  font-size: 13px;
  line-height: 20px;
  color: #555;
}
.flex-wrap .item .link {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 0 10px;
}
.flex-wrap .item .link .btn {
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  margin: 0 2px;
}
</style>