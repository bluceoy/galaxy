<template>
    <div class="notice">
        <p class="title">Notice</p>
        <div class="content">
            Update isn't done yet. Please give more time and don't submit new missions untill furthure notice.
            <span class="time">2021/01/15</span>
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
.notice {
    margin-bottom: 40px;
    background: #fffccc;
    padding: 10px;
}
.notice .title {
    font-size: 16px;
    font-weight: bold;
}
.notice .content {
    font-size: 14px;
}
.notice .content .time {
    display: block;
    line-height: 40px;
}
</style>