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
            Sargfam database and profile Hidden Markov Models based alignment algorithm for ARGs-like sequences annotation were a function module in ARGs-OAP v2.0, supporting supplementary sequence retrieval strategy to current similarity search method (i.e. UBLAST and BLAST), especially applied on detecting remote homolog (novel genes).
        </blockquote>
        <p><a @click="onOpen" href="#">Online Analysis</a></p>
        <p><a href="#sargfam-how-to-use">How To Use</a></p>
        <p><a href="#sargfam-under-the-hood">Under the Hood</a></p>
        <p><a href="#sargfam-how-to-cite">How To Cite</a></p>
        <p><a href="#sargfam-contacts">Contacts</a></p>
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