/**
 * base jScrollpane
 * @author jinjian2@myhexin.com
 * @date 2011-03-17
 */
;(function($) {

$.jScrollPane = {
  active : {}
};
$.fn.jScrollPane = function(settings)
{
  var settings = $.extend({}, $.fn.jScrollPane.defaults, settings);
	
  return this.each(
    function(index, ele)
    {
        var win = window,
	    	doc = document,
            self = this,
            $this = $(this).css({'overflow':'hidden'}),
            scrollPaneId = index,
            clientH = $this.height(),
            clientW = $this.width(),
            scrollH = self.scrollHeight,
            scrollW = self.scrollWidth,
            scrollRangV = scrollH-clientH,
            scrollRangH = scrollW-clientW,
            $container,
            $trackV,
            $trackH,
            $thumbV,
            $thumbH,
            oldMouseY = 0,
            oldMouseX = 0,
            dragPosition = 0,
            dragPositionH = 0,
            trackHeight,
            trackWidth,
            thumbHeight,
            thumbWidth,
            thumbRang,
            thumbRangH,
            thumbMin = 0,
            mouseWheelMultiplier = settings.wheelSpeed,
            currentArrowDirection,
            currentPageDirection,
            currentArrowInc,
            scrollEffectTimer,
            theScrollPane,
            resetTimer,
	    	isDragging = false,
            /**
             * 榧犳爣绉诲叆婊氬姩鍖哄煙鏁堟灉
             */
            scrollHoverEffect = function(){
              if(!$trackV 
                  || !$.isFunction($trackV.stop) 
                  || ($.browser.msie && $.browser.version == "8.0")     //IE8.0婊ら暅BUG
		  		  || isDragging
                ) return;
              if($trackV) $trackV.stop().animate({"opacity":1});
              if($trackH) $trackH.stop().animate({"opacity":1});
            },
            /**
             * 榧犳爣绉诲嚭婊氬姩鍖哄煙鏁堟灉
             */
            scrollBlurEffect = function(){
              if(!$trackV 
                || !$.isFunction($trackV.stop)
                || ($.browser.msie && $.browser.version == "8.0")  //IE8.0婊ら暅BUG
				|| isDragging
                ) return;
              
              if($trackV) $trackV.stop().animate({"opacity":0.75});
              if($trackH) $trackH.stop().animate({"opacity":0.75});
            };
        	
        if(!$this.attr("data-jscrollid")){
          	$this.attr("data-jscrollid","jscroll_"+self.id||(new Date()).getTime());
        }
        
		scrollPaneId = $this.attr("data-jscrollid")+"_"+index;
		
		if($.jScrollPane.active[scrollPaneId]){
			theScrollPane = $.jScrollPane.active[scrollPaneId];
		}else{
			$.jScrollPane.active[scrollPaneId] = theScrollPane = {};
		}
		
        if ($this.parent().is('.jScrollPaneContainer')) {
			$container = $(this).parent('.jScrollPaneContainer');
			
			if(settings.scrollArea){
				$(settings.scrollArea).unbind('mousewheel.jScrollPaneDragging');
			}
			$container.unbind();
			$('>.jScrollPaneTrackV, >.jScrollArrowUpV, >.jScrollArrowDownV,>.jScrollPaneTrackH, >.jScrollArrowUpH, >.jScrollArrowDownH', $container).unbind().remove();
			$this.css({'top':0});
        }else{
			//$this.data('originalStyleTag', $this.attr('style')).css({'overflow':'hidden','position':'absolute','left':'0','top':'0'});
			$this.data('originalStyleTag', $this.attr('style')).css({'overflow':'hidden'});
			$container = $('<div class="jScrollPaneContainer" tabindex="'+settings.tabIndex+'"></div>');
			$this.wrap($container);
			$container = $this.parent();
			
			$(window).unbind("resize.jScrollPaneDragging").bind("resize.jScrollPaneDragging", function(event){
				$this.jScrollPane(settings);
			});
       }
        $this.css('width' ,930);
		$container.css({'overflow':'hidden','height':$this.css('height')||"",'width':$this.css('width')||""}).scrollTop(0);
		$(document).scrollTop(0);
	
     //妯悜婊氬姩鏉�
		/**
		 * 鍐呭瀹藉害鏈夊彉鍖栨椂鏀瑰彉妯悜婊氬姩鏉�
		 */
		var changeScrollH = function(){
				if(!$trackH || !$thumbH) return; 
		
				trackWidth = $trackH.width();
				thumbWidth = clientW/scrollW*trackWidth;
				thumbRangH = trackWidth - thumbWidth;
		
				dragPositionH = Math.max($this.scrollLeft(), $this.data('scrollLeft')||0);
				var p = dragPositionH/scrollRangH;	//(self.scrollLeft||0)/scrollRangH;
		
				if(dragPositionH < 0 || clientW >= scrollW){
					dragPositionH = 0;
				}else if(dragPositionH > scrollRangH){
					dragPositionH = scrollRangH;
				}
		
				//$this.css({"left":(-1*dragPositionH)+"px"});
				$this.scrollLeft(dragPositionH);
		
				$thumbH.css({"width":thumbWidth+"px","height":settings.scrollbarWidth+"px","left":(p*thumbRangH)+"px"});
			};
		
		    if(scrollRangH > 0.99 && settings.scrollBarH){
			$container.append('<div class="jScrollPaneTrackH" id="jScrollPaneTrackH_'+scrollPaneId+'"><div class="jScrollPaneTrackLeftH"></div><div class="jScrollPaneTrackRightH"></div><div class="jScrollPaneDragH" id="jScrollPaneDragH_'+scrollPaneId+'"><div class="jScrollPaneDragTopH"></div><div class="jScrollPaneDragBottomH"></div></div></div>');
			$this.css({'padding-bottom':settings.scrollbarWidth+'px'});
			$trackH = $('#jScrollPaneTrackH_'+scrollPaneId, $container);
			$thumbH = $('#jScrollPaneDragH_'+scrollPaneId,$container);
			  
			$thumbH.bind("mousedown.jScrollPaneDragging",startDragH);
			$trackH.bind("mouseup.jScrollPaneDragging",endDragH)
				.bind("click.jScrollPaneDragging",clickStrackH);
			$(doc).bind("mouseup.jScrollPaneDragging",endDragH);
			  
			var trackHCap = (scrollRangV > 0.99 && settings.scrollBarV)?settings.scrollbarWidth:0,
				  trackHCapLeft = $('.jScrollPaneTrackLeftH',$trackH).width()||0,
				  trackHCapRight = $('.jScrollPaneTrackRightH',$trackH).width()||0;
			  
			if(settings.trackShowCap){
				$('.jScrollPaneTrackLeftH',$trackH).css({'left':(-1*trackHCapLeft)+'px'});
				$('.jScrollPaneTrackRightH',$trackH).css({'right':(-1*trackHCapRight)+'px'});
			}else{
				trackHCapLeft = 0;
				trackHCapRight = 0;
			}
			  
			$trackH.css({'width':(clientW-trackHCap-trackHCapLeft-trackHCapRight)+"px",'height':settings.scrollbarWidth+"px",'left':trackHCapLeft+'px'});
			changeScrollH();
		    }else{
			$this.data('scrollLeft', 0);
		}
		    
    //绾靛悜婊氬姩鏉� 
	/**
	 * 鍐呭楂樺害鍙樺寲鏃舵敼鍙樻粴鍔ㄦ潯
	 */
	var changeScrollV = function(){
		if(!$trackV || !$thumbV ) return;
		
		trackHeight = $trackV.height();
		thumbHeight = clientH/scrollH*trackHeight;
		thumbRang = trackHeight - thumbHeight;
	
		dragPosition = Math.max($this.scrollTop(), $this.data('scrollTop')||0);
		if(dragPosition < 0 || clientH >= scrollH){
			dragPosition = 0;
		}else if(dragPosition > scrollRangV){
			dragPosition = scrollRangV;
		}
		
		//$this.css({"top":(-1*dragPosition)+"px"});
		$this.scrollTop(dragPosition);
		$thumbV.css({"height":thumbHeight+"px","width":settings.scrollbarWidth+"px","top":(thumbRang*dragPosition/scrollRangV)+"px"});
	};
	
	var _scrollHoverEffectDelegate = function(){ if($.isFunction(scrollHoverEffect)) scrollHoverEffect(); },
		_scrollBlurEffectDelegate = function(){ if($.isFunction(scrollBlurEffect)) scrollBlurEffect(); };
		
	
	/**
	 * 绉诲姩鍒版寚瀹氱殑婊氬姩浣嶇疆
	 */
   var positionDrag = function(pos, moveThumb){
			moveThumb = (moveThumb == undefined)?true:moveThumb;
			  
			if(pos < 0 || isNaN(pos)){
				pos = 0;
			}else if(pos > scrollRangV){
				pos = scrollRangV;
			}
			
			  dragPosition = pos;
			  //$this.css({'top':(-1*dragPosition)+'px'});
			  dragPosition = self.scrollTop = dragPosition;
			  $this.data('scrollTop',dragPosition).trigger('scroll');
			  
			var p = dragPosition/scrollRangV;
			if(p <= 0 || isNaN(p)){
				p = 0;
			}else if(p >= 1){
				p = 1;
			}
			if(moveThumb){
				$thumbV.css({top:(thumbRang*p+thumbMin)+"px"});
			}
			if (settings.showArrows) {
				$upArrow[p == 0 ? 'addClass' : 'removeClass']('disabled');
				$downArrow[p == 1 ? 'addClass' : 'removeClass']('disabled');
			}
        },
        /**
         * 婊氬姩瑙﹀彂浜嬩欢
         */
        startDrag = function(event){
			isDragging = true;
          oldMouseY = event.clientY;
          $(doc).bind("mousemove.jScrollPaneDragging",dragMove);
          
          if(event.preventDefault){
              event.preventDefault();
          }
          return false;
        },
        /**
         * 鐐瑰嚮Track婊氬姩浜嬩欢
         */
        clickStrack = function(event){
          if($(event.target).is(".jScrollPaneTrackV")){
            var oldTop = isNaN(parseInt($thumbV.position().top))?0:parseInt($thumbV.position().top),
                p = 0;
            
            if(event.offsetY>oldTop){
              p = 1;
            }else if(event.offsetY<oldTop){
              p = -1;
            }else{
              p = 0;
            }
            
            positionDrag(dragPosition+thumbHeight*p);
          }
          
          if(event.preventDefault){
              event.preventDefault();
          }
          return false;
        },
        /**
         * 鎷栧姩婊氬姩婊戝潡
         */
        dragMove = function(event){
			if($thumbV.length <= 0 || $thumbV.offsetParent().length <= 0) return;
           var 	pos = $thumbV.position(),
           			oldTop = isNaN(parseInt(pos.top))?thumbMin:parseInt(pos.top);
           if(!oldMouseY){
             oldMouseY = event.clientY;
           }
           var newTop = oldTop+event.clientY-oldMouseY;
           var p = newTop/thumbRang;
           if(p < 0){
             p = 0;
             newTop = 0;
           }else if(p > 1){
             p = 1;
             newTop = thumbRang; 
           }
           
           if(p >= 0 && p <= 1){
			   	   $thumbV.css({top:newTop+"px"});
			 	     positionDrag(scrollRangV*p, false);
			 	     oldMouseY = event.clientY;
			     }
           
           if(event.preventDefault){
              event.preventDefault();
            }
            return false;
        },
        /**
         * 缁撴潫婊氬姩
         */
        endDrag = function(event){
			isDragging = false;
          $(doc).unbind("mousemove.jScrollPaneDragging",dragMove);
        },
        /**
         * 榧犳爣婊氳疆婊氬姩
         */
        mouseWheel = function(event, delta) {
            delta = delta || (event.wheelDelta ? event.wheelDelta / 120 : (event.detail) ?
-event.detail/3 : 0);
            if(dragPosition==null || isNaN(dragPosition)) dragPosition = self.scrollTop||0;	//$this.data("scrollTop")||0; 
			
            var d = dragPosition;
            positionDrag(dragPosition - delta * mouseWheelMultiplier);
            var dragOccured = d != dragPosition;
            
            return !dragOccured;
        },
        
        /**
         * 鏂瑰悜绠ご婊氬姩
         */
        whileArrowButtonDown = function(){
          if (currentArrowInc > 4 || currentArrowInc % 4 == 0) {
            positionDrag(dragPosition + currentArrowDirection * mouseWheelMultiplier);
          }
          currentArrowInc++;
        },
        
        /**
         * PageDown/PageUp婊氬姩澶勭悊
         */
        whilePageButtonDown = function(){
            positionDrag(dragPosition+thumbHeight*currentPageDirection);
        },
        
         /**
         * 妯悜绉诲姩鍒版寚瀹氱殑婊氬姩浣嶇疆
         */
        positionDragH = function(pos, moveThumb){
			var p = pos/scrollRangH;
			moveThumb = (moveThumb == undefined)?true:moveThumb;
			if(p <= 0 || isNaN(p)){
				p = 0;
			}else if(p >= 1){
				p = 1;
			}
			  
			dragPositionH = p*scrollRangH;
			$this.css({'left':(-1*dragPositionH)+'px'});
			//self.scrollLeft = dragPositionH;
			$this.data('scrollLeft',dragPositionH).trigger('scroll');
			if(moveThumb){
				$thumbH.css({left:(thumbRangH*p+thumbMin)+"px"});
			}
          
        },
        /**
         * 婊氬姩瑙﹀彂浜嬩欢
         */
        startDragH = function(event){
          oldMouseX = event.clientX;
          $(doc).bind("mousemove.jScrollPaneDragging",dragMoveH);
          isDragging = true;
          if(event.preventDefault){
              event.preventDefault();
          }
          return false;
        },
        /**
         * 鐐瑰嚮Track婊氬姩浜嬩欢
         */
        clickStrackH = function(event){
          if($(event.target).is(".jScrollPaneTrackH")){
            var oldLeft = isNaN(parseInt($thumbH.position().left))?0:parseInt($thumbH.position().left),
                p = 0;
            
            if(event.offsetX>oldLeft){
              p = 1;
            }else if(event.offsetX<oldLeft){
              p = -1;
            }else{
              p = 0;
            }
            
            positionDragH(dragPositionH+thumbWidth*p);
          }
          
          if(event.preventDefault){
              event.preventDefault();
          }
          return false;
        },
        /**
         * 鎷栧姩婊氬姩婊戝潡
         */
        dragMoveH = function(event){
			if($thumbH.length <= 0 || $thumbH.offsetParent().length <= 0) return;
           var pos = $thumbH.position(),
           		 oldLeft = isNaN(parseInt(pos.left))?thumbMin:parseInt(pos.left);
           if(!oldMouseX){
             oldMouseX = event.clientX;
           }
           var newLeft = oldLeft+event.clientX-oldMouseX;
           var p = newLeft/thumbRangH;
		   
           if(p < 0){
             p = 0;
             newLeft = 0;
           }else if(p > 1){
             p = 1;
             newLeft = thumbRangH; 
           }
           
           if(p >= 0 && p <= 1){
             $thumbH.css({left:newLeft+"px"});
             positionDragH(scrollRangH*p, false);
             oldMouseX = event.clientX;
           }
           
           if(event.preventDefault){
              event.preventDefault();
            }
            return false;
        },
        /**
         * 缁撴潫婊氬姩
         */
        endDragH = function(event){
		  	isDragging = false;
			$(doc).unbind("mousemove.jScrollPaneDragging",dragMoveH);
        };
	
	if(scrollRangV > 0.99 && settings.scrollBarV){
		$container.append('<div class="jScrollPaneTrackV" id="jScrollPaneTrackV_'+scrollPaneId+'"><div class="jScrollPaneDragV" id="jScrollPaneDragV_'+scrollPaneId+'"></div></div>');
		  
		$trackV = $('#jScrollPaneTrackV_'+scrollPaneId, $container);
		$thumbV = $('#jScrollPaneDragV_'+scrollPaneId,$container);
		
		$thumbV.bind("mousedown.jScrollPaneDragging",startDrag);
		$trackV.bind("mouseup.jScrollPaneDragging",endDrag)
			.bind("click.jScrollPaneDragging",clickStrack);
		$(doc).bind("mouseup.jScrollPaneDragging",endDrag);
		$container.hover(_scrollHoverEffectDelegate,_scrollBlurEffectDelegate);
		if(settings.scrollArea){
			$(settings.scrollArea).bind('mousewheel.jScrollPaneDragging', mouseWheel);
		}else{
			$container.bind('mousewheel.jScrollPaneDragging', mouseWheel);
		}
		  
		var trackVCap = (scrollRangH > 0.99 && settings.scrollBarH || $trackH)?settings.scrollbarWidth:0,
		      trackVCapTop = settings.trackVCapTop||0,//$('.jScrollPaneTrackTopV',$trackV).height()||0,
		      trackVCapBottom = settings.trackVCapBottom||0;//$('.jScrollPaneTrackBottomV',$trackV).height()||0;
		  
		if(settings.trackShowCap){
		    $('.jScrollPaneTrackTopV',$trackH).css({'top':(-1*trackVCapTop)+'px'});
		    $('.jScrollPaneTrackBottomV',$trackH).css({'bottom':(-1*trackVCapBottom)+'px'});
		}else{
		    trackVCapTop = 0;
		    trackVCapBottom = 0;
		}
		  
		$trackV.css({'height':(clientH-trackVCap-trackVCapBottom-trackVCapTop)+"px",'width':settings.scrollbarWidth+"px",'top':trackVCapTop+'px'});
			changeScrollV();
        }else{
			$this.data('scrollTop',0);
		}
       
        if($.isFunction(scrollBlurEffect)){
          if(scrollEffectTimer) clearTimeout(scrollEffectTimer);
          scrollEffectTimer = setTimeout(scrollBlurEffect, 1000); 
        }
        
		var _scrollKeyDownDelegate = function(e){
		  switch (e.keyCode) {
			case 38: //up
			  currentArrowDirection = -1;
			  currentArrowInc = 0;
			  whileArrowButtonDown();
			  return false;
			case 40: //down
			  currentArrowDirection = 1;
			  currentArrowInc = 0;
			  whileArrowButtonDown();
			  return false;
			case 33: // page up
			  currentPageDirection = -1;
			  whilePageButtonDown();
			  return false;
			case 34: // page down
			  currentPageDirection = 1;
			  whilePageButtonDown();
			  return false;
			default:
		  }
		};

        if (settings.enableKeyboardNavigation) {
          $container.bind('keydown.jScrollPaneDragging', _scrollKeyDownDelegate);
        }
        
        if (settings.showArrows && $trackV) {
          
          var currentArrowButton,
              currentArrowInterval,
              onArrowMouseUp = function(event)
              {
                $('html').unbind('mouseup', onArrowMouseUp);
                currentArrowButton.removeClass('jScrollActiveArrowButton');
                clearInterval(currentArrowInterval);
              },
              onArrowMouseDown = function() {
                $('html').bind('mouseup', onArrowMouseUp);
                currentArrowButton.addClass('jScrollActiveArrowButton');
                currentArrowInc = 0;
                whileArrowButtonDown();
                currentArrowInterval = setInterval(whileArrowButtonDown, 100);
              },
			  _arrowUpMouseDownDelegate = function(){
				  currentArrowButton = $(this);
				  currentArrowDirection = -1;
				  onArrowMouseDown();
				  this.blur();
				  return false;
				},
			  _arrowDownMouseDownDelegate = function()
                {
                  currentArrowButton = $(this);
                  currentArrowDirection = 1;
                  onArrowMouseDown();
                  this.blur();
                  return false;
                };
          
          $trackV.append(
              $('<a href="javascript:;" class="jScrollArrowUpV" tabindex="-1">Scroll up</a>')
                .css(
                  {
                    'width':settings.scrollbarWidth+'px',
                    'top':settings.topCapHeight + 'px'
                  }
                )
                .bind('mousedown', _trackVMouseDownDelegate),
              $('<a href="javascript:;" class="jScrollArrowDownV" tabindex="-1">Scroll down</a>')
                .css(
                  {
                    'width':settings.scrollbarWidth+'px',
                    'bottom':settings.bottomCapHeight + 'px'
                  }
                )
                .bind('mousedown', _arrowDownMouseDownDelegate)
            );
          var $upArrow = $('>.jScrollArrowUpV', $trackV),
              $downArrow = $('>.jScrollArrowDownV', $trackV);
              
          trackHeight = $trackV.height()-$upArrow.outerHeight()-$downArrow.outerHeight();
          thumbHeight = clientH/scrollH*trackHeight;
          thumbRang = trackHeight - thumbHeight;
          thumbMin = $upArrow.outerHeight();
          $thumbV.css({top:thumbMin+"px"});
        }
        
		
		var checkSizeTimer = theScrollPane["checkSizeTimer"]||-1;
		if(checkSizeTimer) clearInterval(checkSizeTimer);
		theScrollPane["checkSizeTimer"] = checkSizeTimer = setInterval(function(){
			if(!self) return;
			var 	newScrollTop = self.scrollTop,
					newScrollLeft = self.scrollLeft,
					newHeight = self.scrollHeight,
					newWidth = self.scrollWidth;
	
			if(Math.abs(newHeight - scrollH) > 0.99){
				scrollH = newHeight;
				scrollRangV = scrollH - clientH;
				if($trackV && $thumbV && scrollRangV > 0.99){
					changeScrollV();
				}else{
					$this.jScrollPane(settings);
				}
			}
			if(newScrollTop != dragPosition){
				positionDrag(newScrollTop);
			}
			if(newScrollLeft != dragPositionH){
				positionDragH(newScrollLeft);
			}
			if(Math.abs(newWidth - scrollW) > 0.99){
				scrollW = newWidth;
				scrollRangH = scrollW - clientW;
				if($trackH && $thumbH && scrollRangH > 0.99){
					changeScrollH();
				}else{
					$this.jScrollPane(settings);
				}
			}
		}, 300);
		var _windowUnloadDelegate = function(){
			var checkSizeTimer = theScrollPane["checkSizeTimer"]||-1;
			if(checkSizeTimer) clearInterval(checkSizeTimer);
			theScrollPane["checkSizeTimer"] = null;
			
			if($thumbH) $thumbH.unbind();
			if($trackH) $trackH.unbind().remove();
			$(doc).unbind("mouseup.jScrollPaneDragging");
			
			if($thumbV) $thumbV.unbind();
			if($trackV) $trackV.unbind().remove();
			$(doc).unbind("mouseup.jScrollPaneDragging");
			if($container) $container.unbind().remove();
			
			$container = null;
			scrollHoverEffect = null;
			scrollBlurEffect = null;
			for(var key in settings){
				settings[key] = null;
			}
			settings = null;
			$(window).unbind("unload.jScrollPaneDragging");
        };
		$(window).unbind("unload.jScrollPaneDragging").bind("unload.jScrollPaneDragging", _windowUnloadDelegate);
    }
  )
};


$.fn.jScrollPane.defaults = {
  scrollbarWidth : 12,
  scrollbarMargin : 0,
  wheelSpeed : 48,
  showArrows : false,
  animateTo : false,
  animateInterval : 100,
  animateStep: 3,
  maintainPosition: true,
  scrollArea: null,
  scrollbarOnLeft: false,
  scrollBarV:true,
  scrollBarH:false,
  reinitialiseOnImageLoad: false,
  tabIndex : -1,
  enableKeyboardNavigation: false,
  animateToInternalLinks: false,
  observeHash: true,
  trackVCapTop: 5,
  trackVCapBottom: 5,
  trackShowCap: true,
  id:0
};

})(jQuery);
