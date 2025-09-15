<template>
  <button
    :type="type"
    :disabled="disabled || loading || readonly"
    :class="buttonClasses"
    @click="handleClick"
  >
    <span v-if="loading" class="kycp-button__spinner"></span>
    <slot>{{ label }}</slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  label?: string
  scriptId?: string
  variant?: 'primary' | 'secondary' | 'text'
  size?: 'small' | 'medium' | 'large'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  readonly?: boolean
  fullWidth?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'secondary',
  size: 'medium',
  type: 'button',
  disabled: false,
  loading: false,
  readonly: false,
  fullWidth: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
  trigger: [scriptId: string]
}>()

const handleClick = (event: MouseEvent) => {
  // In read-only mode, buttons do nothing
  if (props.readonly) {
    event.preventDefault()
    return
  }
  
  emit('click', event)
  
  // Emit scriptId for KYCP button actions
  if (props.scriptId) {
    emit('trigger', props.scriptId)
  }
}

const buttonClasses = computed(() => {
  return [
    'kycp-button',
    `kycp-button--${props.variant}`,
    `kycp-button--${props.size}`,
    {
      'kycp-button--loading': props.loading,
      'kycp-button--disabled': props.disabled,
      'kycp-button--full-width': props.fullWidth
    }
  ]
})
</script>

<style scoped>
.kycp-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: var(--kycp-font-family);
  font-weight: 500;
  border-radius: 3px;
  transition: all 0.2s;
  cursor: pointer;
  border: 1px solid transparent;
  position: relative;
}

/* Sizes */
.kycp-button--small {
  padding: 6px 12px;
  font-size: 13px;
  line-height: 1.4;
}

.kycp-button--medium {
  padding: 10px 20px;
  font-size: 14px;
  line-height: 1.4;
}

.kycp-button--large {
  padding: 12px 24px;
  font-size: 16px;
  line-height: 1.4;
}

/* Primary variant - Blue like "UPLOAD" button */
.kycp-button--primary {
  background: var(--kycp-primary);
  color: var(--kycp-white);
  border-color: var(--kycp-primary);
}

.kycp-button--primary:hover:not(:disabled) {
  background: var(--kycp-primary-hover);
  border-color: var(--kycp-primary-hover);
}

.kycp-button--primary:active:not(:disabled) {
  transform: translateY(1px);
}

/* Secondary variant - Light like "CANCEL" button */
.kycp-button--secondary {
  background: var(--kycp-white);
  color: var(--kycp-primary);
  border-color: var(--kycp-input-border);
}

.kycp-button--secondary:hover:not(:disabled) {
  background: var(--kycp-gray-50);
  border-color: var(--kycp-primary);
}

/* Text variant - No border */
.kycp-button--text {
  background: transparent;
  color: var(--kycp-primary);
  border-color: transparent;
  padding-left: 8px;
  padding-right: 8px;
}

.kycp-button--text:hover:not(:disabled) {
  text-decoration: underline;
}

/* States */
.kycp-button:disabled,
.kycp-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.kycp-button--loading {
  color: transparent;
}

.kycp-button--full-width {
  width: 100%;
}

/* Loading spinner */
.kycp-button__spinner {
  position: absolute;
  width: 14px;
  height: 14px;
  border: 2px solid var(--kycp-gray-300);
  border-top-color: var(--kycp-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.kycp-button--primary .kycp-button__spinner {
  border-color: rgba(255, 255, 255, 0.3);
  border-top-color: var(--kycp-white);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>