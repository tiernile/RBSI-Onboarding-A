<template>
  <div class="kycp-accordion">
    <div 
      v-for="(section, index) in sections" 
      :key="section.id || index"
      class="kycp-accordion__section"
      :class="{ 
        'kycp-accordion__section--expanded': expandedSections[index],
        'kycp-accordion__section--collapsed': !expandedSections[index]
      }"
    >
      <!-- Section Header -->
      <button
        type="button"
        class="kycp-accordion__header"
        @click="toggleSection(index)"
        :aria-expanded="expandedSections[index] ? 'true' : 'false'"
        :aria-controls="`section-content-${index}`"
      >
        <span class="kycp-accordion__icon">
          <svg 
            class="kycp-accordion__chevron" 
            :class="{ 'kycp-accordion__chevron--expanded': expandedSections[index] }"
            width="16" 
            height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </span>
        <span class="kycp-accordion__title">{{ section.title }}</span>
      </button>

      <!-- Section Content -->
      <Transition name="accordion">
        <div 
          v-show="expandedSections[index]"
          :id="`section-content-${index}`"
          class="kycp-accordion__content"
        >
          <div class="kycp-accordion__inner">
            <div v-if="section.description" class="kycp-accordion__description">
              {{ section.description }}
            </div>
            <slot :name="`section-${index}`" :section="section" :index="index">
              <slot name="default" :section="section" :index="index">
                <!-- Default content if no specific slot provided -->
                <div class="kycp-accordion__placeholder">
                  Section content goes here
                </div>
              </slot>
            </slot>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface AccordionSection {
  id?: string
  title: string
  description?: string
  expanded?: boolean
}

interface Props {
  sections: AccordionSection[]
  multiple?: boolean // Allow multiple sections open at once
  expandFirst?: boolean // Expand first section by default
  expandAll?: boolean // Expand all sections by default
}

const props = withDefaults(defineProps<Props>(), {
  multiple: true,
  expandFirst: false,
  expandAll: false
})

const emit = defineEmits<{
  'section-toggle': [index: number, expanded: boolean]
  'section-expand': [index: number]
  'section-collapse': [index: number]
}>()

// Track which sections are expanded
const expandedSections = ref<Record<number, boolean>>({})

// Initialize expanded state
onMounted(() => {
  props.sections.forEach((section, index) => {
    if (props.expandAll) {
      expandedSections.value[index] = true
    } else if (props.expandFirst && index === 0) {
      expandedSections.value[index] = true
    } else if (section.expanded) {
      expandedSections.value[index] = true
    } else {
      expandedSections.value[index] = false
    }
  })
})

// Toggle section expanded/collapsed state
const toggleSection = (index: number) => {
  const isExpanded = expandedSections.value[index]
  
  if (!props.multiple && !isExpanded) {
    // If not multiple, collapse all others first
    Object.keys(expandedSections.value).forEach(key => {
      expandedSections.value[Number(key)] = false
    })
  }
  
  expandedSections.value[index] = !isExpanded
  
  emit('section-toggle', index, expandedSections.value[index])
  if (expandedSections.value[index]) {
    emit('section-expand', index)
  } else {
    emit('section-collapse', index)
  }
}

// Public methods via expose
const expandSection = (index: number) => {
  expandedSections.value[index] = true
  emit('section-expand', index)
}

const collapseSection = (index: number) => {
  expandedSections.value[index] = false
  emit('section-collapse', index)
}

const expandAllSections = () => {
  props.sections.forEach((_, index) => {
    expandedSections.value[index] = true
  })
}

const collapseAllSections = () => {
  props.sections.forEach((_, index) => {
    expandedSections.value[index] = false
  })
}

defineExpose({
  expandSection,
  collapseSection,
  expandAllSections,
  collapseAllSections,
  expandedSections
})
</script>

<style scoped>
.kycp-accordion {
  margin-bottom: var(--kycp-spacing-xl, 32px);
}

.kycp-accordion__section {
  margin-bottom: 2px;
  background: var(--kycp-white, #ffffff);
  overflow: hidden;
}

.kycp-accordion__section:first-child {
  border-radius: var(--kycp-radius-base, 3px) var(--kycp-radius-base, 3px) 0 0;
}

.kycp-accordion__section:last-child {
  border-radius: 0 0 var(--kycp-radius-base, 3px) var(--kycp-radius-base, 3px);
}

.kycp-accordion__section:only-child {
  border-radius: var(--kycp-radius-base, 3px);
}

.kycp-accordion__header {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 14px 16px;
  background: #7fb3d5; /* Light blue color from image */
  color: var(--kycp-white, #ffffff);
  border: none;
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease;
  position: relative;
}

.kycp-accordion__header:hover {
  background: #6fa3c5; /* Slightly darker on hover */
}

.kycp-accordion__header:focus {
  outline: none;
  box-shadow: inset 0 0 0 2px var(--kycp-focus, #0969da);
}

.kycp-accordion__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  flex-shrink: 0;
}

.kycp-accordion__chevron {
  transition: transform 0.2s ease;
  transform: rotate(0deg);
}

.kycp-accordion__chevron--expanded {
  transform: rotate(90deg);
}

.kycp-accordion__title {
  flex: 1;
  margin-right: 12px;
}

.kycp-accordion__content {
  background: var(--kycp-white, #ffffff);
  border: 1px solid var(--kycp-gray-200, #e5e7eb);
  border-top: none;
}

.kycp-accordion__inner {
  padding: 20px;
}

.kycp-accordion__description {
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--kycp-gray-600, #6b7280);
  line-height: 1.5;
}

.kycp-accordion__placeholder {
  padding: 12px;
  background: var(--kycp-gray-50, #f9fafb);
  border: 1px dashed var(--kycp-gray-300, #d1d5db);
  border-radius: 3px;
  color: var(--kycp-gray-500, #6b7280);
  font-size: 13px;
  text-align: center;
}

/* Transition animations */
.accordion-enter-active,
.accordion-leave-active {
  transition: all 0.3s ease;
  max-height: 1000px;
  overflow: hidden;
}

.accordion-enter-from,
.accordion-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
}

/* Accessibility - Focus visible */
.kycp-accordion__header:focus-visible {
  outline: 2px solid var(--kycp-focus, #0969da);
  outline-offset: 2px;
}

/* Print styles */
@media print {
  .kycp-accordion__section {
    break-inside: avoid;
  }
  
  .kycp-accordion__content {
    display: block !important;
  }
  
  .kycp-accordion__chevron {
    display: none;
  }
}
</style>