<script>
    (function () {
        var ref = Vue.ref;
        var reactive = Vue.reactive;
        var computed = Vue.computed;

        // 纯函数区（与 Vue 无关，可单元测试）
        function createEmptyHero() {
            return { id: 0, name: '', hp: '' }; // 表单阶段 hp 用字符串，提交时转换
        }

        function prepareHeroName(name, id) {
            var s = String(name == null ? '' : name).trim();
            if (s.length > 0) {
                return s;
            }
            return 'Hero#' + id;
        }

        function prepareHeroHp(hp) {
            var n = Number(hp);
            if (Number.isFinite(n) && n >= 0) {
                return Math.floor(n);
            }
            return 0;
        }

        function findHeroIndexById(list, heroId) {
            var i;
            for (i = 0; i < list.length; i = i + 1) {
                if (list[i].id === heroId) {
                    return i;
                }
            }
            return -1;
        }

        function addHeroToList(list, nextId, draft) {
            var id = nextId + 1;
            var newHero = {
                id: id,
                name: prepareHeroName(draft.name, id),
                hp: prepareHeroHp(draft.hp)
            };
            var newList = list.slice();
            newList.push(newHero);
            return { nextId: id, list: newList };
        }

        function updateHeroInList(list, draft) {
            var idx = findHeroIndexById(list, draft.id);
            if (idx === -1) {
                return list;
            }
            var updated = {
                id: draft.id,
                name: prepareHeroName(draft.name, draft.id),
                hp: prepareHeroHp(draft.hp)
            };
            var copy = list.slice();
            copy.splice(idx, 1, updated);
            return copy;
        }

        function removeHeroFromList(list, heroId) {
            var idx = findHeroIndexById(list, heroId);
            if (idx === -1) {
                return list;
            }
            var copy = list.slice();
            copy.splice(idx, 1);
            return copy;
        }

        // 应用实例
        var app = Vue.createApp({
            setup: function () {
                // 领域状态（不可变列表）
                var heroes = ref([
                    { id: 1, name: '盖伦', hp: 318 },
                    { id: 2, name: '提莫', hp: 320 },
                    { id: 3, name: '安妮', hp: 419 },
                    { id: 4, name: '死歌', hp: 325 },
                    { id: 5, name: '米波', hp: 422 }
                ]);

                var nextId = ref((function () {
                    var maxId = 0;
                    var i;
                    for (i = 0; i < heroes.value.length; i = i + 1) {
                        if (heroes.value[i].id > maxId) {
                            maxId = heroes.value[i].id;
                        }
                    }
                    return maxId;
                })());

                // 表单状态（受控输入）
                var addForm = reactive(createEmptyHero());
                var editForm = reactive(createEmptyHero());
                var editingId = ref(null);

                var isEditing = computed(function () {
                    return editingId.value !== null;
                });

                var editingHero = computed(function () {
                    if (editingId.value === null) {
                        return null;
                    }
                    var i = findHeroIndexById(heroes.value, editingId.value);
                    if (i === -1) {
                        return null;
                    }
                    return heroes.value[i];
                });

                // 受控表单输入处理（显式同步）
                function onAddNameInput(e) {
                    addForm.name = e.target.value;
                }

                function onAddHpInput(e) {
                    addForm.hp = e.target.value;
                }

                function onEditNameInput(e) {
                    editForm.name = e.target.value;
                }

                function onEditHpInput(e) {
                    editForm.hp = e.target.value;
                }

                // 事件：新增
                function submitAdd() {
                    var result = addHeroToList(heroes.value, nextId.value, addForm);
                    heroes.value = result.list;
                    nextId.value = result.nextId;
                    Object.assign(addForm, createEmptyHero());
                }

                // 事件：开始编辑
                function startEditing(heroId) {
                    var h = null;
                    var i = findHeroIndexById(heroes.value, heroId);
                    if (i !== -1) {
                        h = heroes.value[i];
                    }
                    if (!h) {
                        return;
                    }
                    editingId.value = h.id;
                    Object.assign(editForm, {
                        id: h.id,
                        name: h.name,
                        hp: String(h.hp)
                    });
                }

                // 事件：确认编辑
                function submitEdit() {
                    if (editingId.value === null) {
                        return;
                    }
                    // 确保 editForm.id 存在
                    if (typeof editForm.id !== 'number' || editForm.id <= 0) {
                        return;
                    }
                    heroes.value = updateHeroInList(heroes.value, editForm);
                    cancelEditing();
                }

                // 事件：取消编辑
                function cancelEditing() {
                    editingId.value = null;
                    Object.assign(editForm, createEmptyHero());
                }

                // 事件：删除
                function removeHero(heroId) {
                    heroes.value = removeHeroFromList(heroes.value, heroId);
                    if (editingId.value === heroId) {
                        cancelEditing();
                    }
                }

                return {
                    // state
                    heroes: heroes,
                    addForm: addForm,
                    editForm: editForm,
                    isEditing: isEditing,
                    editingHero: editingHero,
                    // handlers
                    onAddNameInput: onAddNameInput,
                    onAddHpInput: onAddHpInput,
                    onEditNameInput: onEditNameInput,
                    onEditHpInput: onEditHpInput,
                    submitAdd: submitAdd,
                    startEditing: startEditing,
                    submitEdit: submitEdit,
                    cancelEditing: cancelEditing,
                    removeHero: removeHero
                };
            }
        });

        app.mount('#app');
    })();
</script>