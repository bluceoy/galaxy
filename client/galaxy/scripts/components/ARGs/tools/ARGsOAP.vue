<template>
    <div>
        <div class="row">
            <div class="col-3">
                <img style="width:90%;" src="/static/args/tools/arg_oap_logo_d.ico" alt="ARGs-OAP logo" >
            </div>
            <h3 class="col-9">
                <strong>ARGs-OAP:</strong> Online Analysis Pipeline for Anti-biotic Resistance Genes Detection from Meta-genomic Data Using an Integrated Structured ARG-database
            </h3>
        </div>
        
        <blockquote>
            Environmental dissemination of antibiotic resistance genes (ARGs) has become an increasing concern for public health. Metagenomics
            approaches can effectively detect broad profiles of ARGs in environmental samples; however, the detection and subsequent
            classification of ARG-like sequences are time consuming and have been severe obstacles in employing metagenomic methods.
            We sought to accelerate quantification of ARGs in metagenomic data from environmental samples.
        </blockquote>

        <p><a @click="onOpen" href="#">Online Analysis</a></p>
        <p><a href="#argoap-how-to-use">How to use</a></p>
        <p><a href="#argoap-downloads">Download</a></p>
        <p><a href="#argoap-faq">FAQ</a></p>
        <p><a href="#argoap-features-change-log">Features Change Log</a></p>
        <p><a href="#argoap-how-to-cite">How To Cite</a></p>
        <p><a href="#argoap-report-error">Report Error</a></p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tool: {
                id: 'addValue',
                version: '1.0.0',
                form_style: 'regular',
                link: '/tool_runner?tool_id=addValue',
                target: 'galaxy_main'
            }
        };
    },
    methods: {
        onOpen(evt) {
            this.$emit('analysis', evt, this.tool);
        }
    }
}
</script>

<style scoped>
</style>