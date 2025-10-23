<script>
    var app = Vue.createApp({
        setup: function () {
            var heroes = Vue.ref([
                { id: 1, name: '盖伦', hp: 318 },
                { id: 2, name: '提莫', hp: 320 },
                { id: 3, name: '安妮', hp: 419 },
                { id: 4, name: '死歌', hp: 325 },
                { id: 5, name: '米波', hp: 422 }
            ]);

            var heroForAdd = Vue.reactive(createEmptyHero());
            var heroForUpdate = Vue.reactive(createEmptyHero());
            var editingIndex = Vue.ref(-1);
            var nextId = Vue.ref(calculateInitialMaxId(heroes.value));

            var isEditing = Vue.computed(function () {
                return editingIndex.value !== -1;
            });

            function createEmptyHero() {
                return { id: 0, name: '', hp: 0 };
            }

            function calculateInitialMaxId(list) {
                var maxId = 0;
                var i;
                for (i = 0; i < list.length; i = i + 1) {
                    if (list[i].id > maxId) {
                        maxId = list[i].id;
                    }
                }
                return maxId;
            }

            function prepareHeroName(name, id) {
                if (name && name.length > 0) {
                    return name;
                }
                return 'Hero#' + id;
            }

            function prepareHeroHp(hp) {
                if (typeof hp === 'number' && !isNaN(hp) && hp >= 0) {
                    return Math.floor(hp);
                }
                return 0;
            }

            function addHero() {
                nextId.value = nextId.value + 1;
                var newHero = {
                    id: nextId.value,
                    name: prepareHeroName(heroForAdd.name, nextId.value),
                    hp: prepareHeroHp(heroForAdd.hp)
                };
                heroes.value.push(newHero);
                Object.assign(heroForAdd, createEmptyHero());
            }

            function findHeroIndexById(heroId) {
                var i;
                for (i = 0; i < heroes.value.length; i = i + 1) {
                    if (heroes.value[i].id === heroId) {
                        return i;
                    }
                }
                return -1;
            }

            function removeHero(heroId) {
                var index = findHeroIndexById(heroId);
                if (index !== -1) {
                    heroes.value.splice(index, 1);
                    if (editingIndex.value === index) {
                        cancelEditing();
                    }
                }
            }

            function startEditing(heroId) {
                var index = findHeroIndexById(heroId);
                if (index === -1) {
                    return;
                }
                editingIndex.value = index;
                Object.assign(heroForUpdate, heroes.value[index]);
            }

            function updateHero() {
                if (editingIndex.value === -1) {
                    return;
                }
                var updatedHero = {
                    id: heroForUpdate.id,
                    name: prepareHeroName(heroForUpdate.name, heroForUpdate.id),
                    hp: prepareHeroHp(heroForUpdate.hp)
                };
                heroes.value.splice(editingIndex.value, 1, updatedHero);
                cancelEditing();
            }

            function cancelEditing() {
                editingIndex.value = -1;
                Object.assign(heroForUpdate, createEmptyHero());
            }

            return {
                heroes: heroes,
                heroForAdd: heroForAdd,
                heroForUpdate: heroForUpdate,
                isEditing: isEditing,
                addHero: addHero,
                removeHero: removeHero,
                startEditing: startEditing,
                updateHero: updateHero,
                cancelEditing: cancelEditing
            };
        }
    });

    app.mount('#app');
</script>