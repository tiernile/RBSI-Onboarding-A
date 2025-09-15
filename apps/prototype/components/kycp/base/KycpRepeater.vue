<template>
  <div class="kycp-repeater">
    <!-- Existing items -->
    <div v-for="(item, index) in items" :key="item.id || index" class="kycp-repeater__item">
      <div class="kycp-repeater__item-header">
        <span class="kycp-repeater__item-title">{{ getItemTitle(item, index) }}</span>
        <button
          type="button"
          class="kycp-repeater__remove"
          @click="removeItem(index)"
          :aria-label="`Remove ${itemLabel}`"
        >
          ×
        </button>
      </div>
      <div class="kycp-repeater__item-content" v-if="expanded[index]">
        <slot name="item" :item="item" :index="index"></slot>
      </div>
    </div>

    <!-- Add new button -->
    <button
      type="button"
      class="kycp-repeater__add"
      @click="addItem"
    >
      ADD NEW...
    </button>

    <!-- Expanded form for new item -->
    <div v-if="showNewForm" class="kycp-repeater__new-item">
      <div class="kycp-repeater__new-header">
        {{ addLabel || `${itemLabel} - Please provide details` }}
      </div>
      <div class="kycp-repeater__new-content">
        <slot name="form" :item="newItem" :save="saveNewItem" :cancel="cancelNewItem"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  modelValue: any[]
  itemLabel?: string
  addLabel?: string
  titleField?: string
  defaultExpanded?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  itemLabel: 'Item',
  defaultExpanded: false
})

const emit = defineEmits<{
  'update:modelValue': [value: any[]]
}>()

// Local state
const showNewForm = ref(false)
const newItem = ref<any>({})
const expanded = ref<Record<number, boolean>>({})

// Computed
const items = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:modelValue', value)
})

// Methods
const getItemTitle = (item: any, index: number): string => {
  if (props.titleField && item[props.titleField]) {
    return item[props.titleField]
  }
  return `${props.itemLabel} ${index + 1}`
}

const addItem = () => {
  showNewForm.value = true
  newItem.value = {}
}

const saveNewItem = () => {
  const updatedItems = [...items.value, { ...newItem.value }]
  emit('update:modelValue', updatedItems)
  showNewForm.value = false
  newItem.value = {}
}

const cancelNewItem = () => {
  showNewForm.value = false
  newItem.value = {}
}

const removeItem = (index: number) => {
  const updatedItems = items.value.filter((_, i) => i !== index)
  emit('update:modelValue', updatedItems)
}

const toggleItem = (index: number) => {
  expanded.value[index] = !expanded.value[index]
}
</script>

<style scoped>
.kycp-repeater {
  margin-bottom: 24px;
}

.kycp-repeater__item {
  background: var(--kycp-white);
  border: 1px solid var(--kycp-input-border);
  border-radius: 3px;
  margin-bottom: 12px;
}

.kycp-repeater__item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--kycp-gray-50);
  border-bottom: 1px solid var(--kycp-input-border);
  cursor: pointer;
}

.kycp-repeater__item-title {
  font-size: 14px;
  color: var(--kycp-gray-900);
  font-weight: 500;
}

.kycp-repeater__remove {
  width: 24px;
  height: 24px;
  padding: 0;
  background: transparent;
  border: none;
  color: var(--kycp-gray-600);
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s;
}

.kycp-repeater__remove:hover {
  color: var(--kycp-error);
}

.kycp-repeater__item-content {
  padding: 16px;
}

.kycp-repeater__add {
  display: block;
  width: 100%;
  padding: 12px;
  background: transparent;
  border: none;
  color: var(--kycp-primary);
  font-size: 14px;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: color 0.2s;
}

.kycp-repeater__add:hover {
  color: var(--kycp-primary-hover);
  text-decoration: underline;
}

.kycp-repeater__new-item {
  background: var(--kycp-white);
  border: 1px solid var(--kycp-section-border);
  border-radius: 3px;
  margin-top: 16px;
  padding: 20px;
}

.kycp-repeater__new-header {
  margin-bottom: 20px;
  font-size: 14px;
  color: var(--kycp-gray-700);
  font-weight: 500;
}

.kycp-repeater__new-content {
  /* Form content goes here */
}
</style>