<template>
    <div :class="shapeClass" :style="shapeStyle">
        <span class="ranking" :style="textStyle">{{ artist.rank_data.ranking }}</span>
    </div>
</template>

<script>
export default {
    name: 'EngagementShape',
    props: {
        artist: {
            type: Object,
            required: true
        },
    },
    computed: {
        shapeStyle() {
            let color;
            if (this.artist.rank_data.percentage > 75) {
                color = 'green';
            } else if (this.artist.rank_data.percentage > 50) {
                color = 'blue';
            } else if (this.artist.rank_data.percentage > 25) {
                color = 'yellow';
            } else {
                color = 'red';
            }
            return {
                backgroundColor: color,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            };
        },
        shapeClass() {
            if (this.artist.rank_data.tier < 10) {
                return 'star';
            } else if (this.artist.rank_data.tier < 20) {
                return 'circle';
            } else {
                return 'square';
            }
        },
        textStyle() {
            return {
                color: this.shapeStyle.backgroundColor === 'yellow' ? 'black' : 'white'
            };
        }
    }
};
</script>

<style scoped>
.circle {
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

.square {
    width: 50px;
    height: 50px;
}

.star {
    height: 80px;
    width: 80px;
    clip-path: polygon(50% 0, 79% 90%, 2% 35%, 98% 35%, 21% 90%);
}

.ranking {
    position: absolute;
    font-size: 20px;
}
</style>