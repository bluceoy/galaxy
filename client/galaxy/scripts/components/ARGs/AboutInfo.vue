<template>
    <div class="flex">
        <div class="logo">
            <img src="/static/args/TeamLogo.png"/>
        </div>
        <div class="text">
            <p>This Galaxy instance is maintained by Environmental Biotechnology Laboratory from the University of Hong Kong. Some pipelines created by the lab are provided here and are free to use for academic purposes.</p>
            <p>The team is led by Prof. Tong Zhang and conducts varied research on ARG, NGS, bioremediation, bioreactor, bioenergy recovery and more.</p>
        </div>
        <div class="btn">
            <a href="/args/about">ABOUT</a>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
        };
    }
}
</script>

<style scoped>
.flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}
.flex .logo {
    width: 120px;
}
.flex .logo img {
    width: 100%;
}
.flex .text {
    width: 65%;
    font-size: 1rem;
    padding-left: 1.5rem;
    margin-left: 20px;
    border-left: 5px solid #ee6e73;
}
.flex .text p {
    margin-top: unset;
}
.flex .text p:last-child {
    margin-bottom: unset;
}
.flex .btn {
    width: 120px;
    font-size: 32px;
}
.flex .btn a {
    text-decoration: none;
}
</style>