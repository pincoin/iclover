class PageableMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PageableMixin, self).get_context_data(**kwargs)
        paginator = context['paginator']
        context['page_all_count'] = paginator.count
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = paginator.page_range[-1]
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class DataSearchFormMixin(object):

    def get_context_data(self, **kwargs):
        context = super(DataSearchFormMixin, self).get_context_data(**kwargs)
        context['data_search_form'] = self.data_search_form(
            q=self.request.GET.get('q') if self.request.GET.get('q') else ''
        )
        if self.request.GET.get('q'):
            context['q'] = self.request.GET.get('q')

        return context